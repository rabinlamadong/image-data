import asyncio

import cv2
import numpy as np
import pandas as pd

from app.db.models import Image
from app.db.session import create_session_manager
from app.settings import settings


async def extract(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


async def transform(data: pd.DataFrame, target_width: int) -> pd.DataFrame:
    depths = data["depth"]
    pixel_data = data.drop(columns=["depth"]).values

    resized_images = []

    for row in pixel_data:
        row = np.array(row, dtype=np.float32).reshape(1, -1)
        if row.shape[1] > 1:
            resized_image = cv2.resize(row, (target_width, 1), interpolation=cv2.INTER_LINEAR)
            resized_images.append(resized_image)
        else:
            print(f"Skipping row with invalid shape: {row.shape}")
            continue

    resized_df = pd.DataFrame(
        np.array(resized_images).reshape(len(resized_images), -1),
        columns=[f"pixel_{i}" for i in range(target_width)],
    )
    resized_df["depth"] = depths.iloc[: len(resized_images)]

    return resized_df


async def load(resized_df: pd.DataFrame) -> None:
    session_manager = create_session_manager(settings)

    async with session_manager() as session:
        async with session.begin():
            for _, row in resized_df.iterrows():
                if not row.any():
                    continue

                image = Image(depth=row["depth"], pixels=row.drop("depth").tolist())
                session.add(image)

        await session.commit()


async def run_etl(file_path: str, target_width: int) -> None:
    data = await extract(file_path)
    resized_df = await transform(data, target_width)
    await load(resized_df)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the ETL process with a CSV file.")
    parser.add_argument("file_path", type=str, help="Path to the CSV file")

    args = parser.parse_args()

    asyncio.run(run_etl(args.file_path, 150))
