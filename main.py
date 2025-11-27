"""
ML Service for IoT Data Classification
High-performance FastAPI service optimized for low-latency predictions
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import time

# Initialize FastAPI app
app = FastAPI(
    title="ML Service - IoT Data Classification",
    description="High-performance microservice for classifying IoT sensor data",
    version="1.0.0"
)

# Add CORS middleware to allow backend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input data model
class SensorData(BaseModel):
    """Input schema for sensor data"""
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage (0-100)")
    co2_level: int = Field(..., ge=0, description="CO2 level in ppm")
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 45.5,
                "humidity": 65,
                "co2_level": 850
            }
        }


# Output data model
class PredictionResponse(BaseModel):
    """Output schema for classification result"""
    label: Literal["HOT", "WARM", "COLD"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    temperature: float
    co2_level: int
    processing_time_ms: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "label": "WARM",
                "confidence": 1.0,
                "temperature": 45.5,
                "co2_level": 850,
                "processing_time_ms": 0.5
            }
        }


def classify_sensor_data(temperature: float, co2_level: int) -> tuple[str, float]:
    """
    Optimized rule-based classification logic
    
    Classification Rules:
    - HOT: temperature > 50 OR co2_level > 1000 (Fire/gas warning)
    - WARM: temperature > 35 (Hot but not dangerous)
    - COLD: All other cases (Normal conditions)
    
    Args:
        temperature: Temperature reading in Celsius
        co2_level: CO2 level in ppm
        
    Returns:
        tuple: (label, confidence) where confidence is always 1.0 for rule-based
    """
    # HOT: Critical conditions - fire or gas hazard
    if temperature > 50 or co2_level > 1000:
        return "HOT", 1.0
    
    # WARM: Elevated temperature
    elif temperature > 35:
        return "WARM", 1.0
    
    # COLD: Normal conditions
    else:
        return "COLD", 1.0


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "ML Service - IoT Data Classification",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {
        "status": "healthy",
        "service": "ml-service-pmnm",
        "timestamp": time.time()
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(sensor_data: SensorData):
    """
    Classify IoT sensor data
    
    Optimized for low latency with in-memory rule-based classification.
    Expected response time: < 10ms
    
    Args:
        sensor_data: Sensor readings (temperature, humidity, co2_level)
        
    Returns:
        PredictionResponse with classification label and metadata
        
    Raises:
        HTTPException: If validation fails
    """
    # Start timing for performance monitoring
    start_time = time.perf_counter()
    
    try:
        # Perform classification (optimized rule-based logic)
        label, confidence = classify_sensor_data(
            temperature=sensor_data.temperature,
            co2_level=sensor_data.co2_level
        )
        
        # Calculate processing time
        processing_time_ms = (time.perf_counter() - start_time) * 1000
        
        # Return prediction response
        return PredictionResponse(
            label=label,
            confidence=confidence,
            temperature=sensor_data.temperature,
            co2_level=sensor_data.co2_level,
            processing_time_ms=round(processing_time_ms, 3)
        )
        
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Classification error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    # Run with optimized settings for low latency
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        log_level="info",
        access_log=True
    )
