Write-Host "?? Starting Podman Engine Subsystem..." -ForegroundColor Cyan
podman machine start

Write-Host "?? Initializing Economic Indicators Dashboard Pod Stack..." -ForegroundColor Cyan
podman pod start economic-pod

Write-Host "?? Application is running! Access the links below:" -ForegroundColor Green
Write-Host "?? Web Dashboard: http://localhost:8081" -ForegroundColor Yellow
Write-Host "?? API Docs:      http://localhost:8000/docs" -ForegroundColor Yellow
