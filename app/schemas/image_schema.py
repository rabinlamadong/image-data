import cv2
from pydantic import BaseModel


class ImageFramesRequestSchema(BaseModel):
    depth_min: float = 0.0
    depth_max: float = 0.0
    colormap: int = cv2.COLORMAP_JET


class ImageFramesResponseSchema(BaseModel):
    pixels: list[list[int]]
    depth: float
    id: int

    class Config:
        from_attributes = True
