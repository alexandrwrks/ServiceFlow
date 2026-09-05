from fastapi import APIRouter

router = APIRouter()


@router.get("/services")
async def get_services(

):
    return await service.get_services()


@router.post("/appointments")
async def appointments(

):
    return await service.appointments()

@router.get("/appointments")
async def get_appointments(

):
    return await service.get_appointments()

@router.patch("/appointments/{id}")
async def update_appointments(

):
    return await service.update_appointments()

@router.get("/clients")
async def get_clients(

):
    return await service.get_clients()

@router.get("/employees")
async def get_employees(

):
    return await service.get_employees()

@router.get("/schedule")
async def get_schedule(

):
    return await service.get_schedule()

@router.post("/schedule")
async def create_schedule(

):
    return await service.create_schedule()

@router.get("/analytics")
async def get_analytics(

):
    return await service.get_analytics()