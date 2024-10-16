import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Image
from app.db.session import create_session_manager
from app.schemas.image_schema import ImageFramesResponseSchema, ImageFramesRequestSchema
from app.settings import settings
from app.utils import apply_colormap_to_frame

router = APIRouter()

session_manager = create_session_manager(settings)


async def get_db() -> AsyncSession:
    async with session_manager() as session:
        yield session


@router.get(
    "/get-image-frames",
    response_model=list[ImageFramesResponseSchema],
)
async def get_image_data(
    params: ImageFramesRequestSchema = Depends(ImageFramesRequestSchema),
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await db.execute(
            select(Image).filter(Image.depth.between(params.depth_min, params.depth_max))
        )
        images = result.scalars().all()

        if not images:
            raise HTTPException(
                status_code=404, detail="No images found in the specified depth range"
            )

        response_data = []

        for image in images:
            pixels = np.array(image.pixels).reshape(1, -1).astype(np.uint8)
            colored_frame = apply_colormap_to_frame(pixels, params.colormap).reshape(-1, 3).tolist()
            response_data.append(
                ImageFramesResponseSchema(id=image.id, depth=image.depth, pixels=colored_frame)
            )

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
