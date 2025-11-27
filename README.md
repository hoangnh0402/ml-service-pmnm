ML Service for IoT Data Classification
Building a high-performance FastAPI microservice to classify IoT sensor data using rule-based logic. The service will be optimized for low latency to handle continuous requests from the backend system.

User Review Required
IMPORTANT

Performance Optimization Strategy The service will use:

In-memory rule-based classification (no model loading overhead)
FastAPI's async capabilities for concurrent request handling
Optimized Docker image with multi-stage builds
Port 5000 as specified in requirements
NOTE

Classification Logic Using rule-based approach instead of ML model for:

Zero model loading time
Sub-millisecond prediction latency
Deterministic results
Easy to understand and maintain
Proposed Changes
Core Application Files
[NEW] 
requirements.txt
Python dependencies with pinned versions for reproducibility:

fastapi[all] - Web framework with all optional dependencies
uvicorn[standard] - ASGI server with performance optimizations
pydantic - Data validation (included with FastAPI)
scikit-learn - For future ML model integration
pandas - Data processing utilities
numpy - Numerical operations
[NEW] 
main.py
Main FastAPI application with optimized endpoints:

SensorData model: Pydantic schema for input validation (temperature, humidity, co2_level)
PredictionResponse model: Structured output with label and confidence
classify_sensor_data(): Optimized rule-based classification function
POST /predict: Main endpoint with async support
GET /health: Health check endpoint for container orchestration
GET /: Root endpoint with API information
CORS middleware: Enable cross-origin requests from backend
Docker Configuration
[NEW] 
Dockerfile
Multi-stage build for optimized image size:

Stage 1 (builder): Install dependencies in virtual environment
Stage 2 (runtime): Minimal runtime image with Python 3.9-slim
Copy only necessary files from builder stage
Non-root user for security
Expose port 5000
Optimized uvicorn command with multiple workers
[NEW] 
.dockerignore
Exclude unnecessary files from Docker build context:

Python cache files (__pycache__, *.pyc)
Virtual environments
Git files
Documentation
Test files
[NEW] 
docker-compose.yml
Local development and testing setup:

Service definition with port mapping (5000:5000)
Environment variables for Uvicorn configuration
Volume mounts for development
Automatic restart policy
Documentation and Support Files
[NEW] 
README.md
Comprehensive documentation including:

Project overview and architecture
API endpoint documentation with examples
Classification logic explanation
Local development setup
Docker deployment instructions
Performance optimization details
Example curl commands and response formats
[NEW] 
.gitignore
Standard Python gitignore patterns:

Python cache and compiled files
Virtual environments
IDE configuration
Environment variables
Log files
Verification Plan
Automated Tests
Start the service locally:

uvicorn main:app --host 0.0.0.0 --port 5000 --reload
Test classification endpoints with various sensor data scenarios:

HOT classification: High temperature (>50) or high CO2 (>1000)
WARM classification: Medium temperature (35-50)
COLD classification: Normal conditions
Edge cases: Exact threshold values
Test health endpoint:

curl http://localhost:5000/health
Docker Verification
Build Docker image:

docker build -t ml-service-pmnm .
Run container:

docker run -p 5000:5000 ml-service-pmnm
Test API through container:

Verify endpoints are accessible
Check response times for latency optimization
Performance Testing
Measure average response time for classification requests
Should be < 10ms for rule-based classification
Verify concurrent request handling
