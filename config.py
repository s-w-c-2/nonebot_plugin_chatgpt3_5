from pydantic import BaseSettings
import os


class Config(BaseSettings):
    # Your Config Here
    class Config:
        priority = 997

    

    