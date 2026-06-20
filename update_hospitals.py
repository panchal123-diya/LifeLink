import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_project.settings')
django.setup()

from hospitals.models import Hospital

real_hospitals = [
    {"name": "Zydus Hospital", "lat": 23.0642, "lng": 72.5173, "phone": "+91 79 6619 0201", "image": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "Apollo Hospitals, Bhat", "lat": 23.1090, "lng": 72.6074, "phone": "+91 79 6670 1800", "image": "https://images.unsplash.com/photo-1551076805-e1869043e560?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "Marengo CIMS Hospital", "lat": 23.0766, "lng": 72.5186, "phone": "+91 79 4805 1200", "image": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "SAL Hospital", "lat": 23.0487, "lng": 72.5204, "phone": "+91 79 6611 5600", "image": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "Sterling Hospital", "lat": 23.0489, "lng": 72.5222, "phone": "+91 79 4001 1111", "image": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "KD Hospital", "lat": 23.1493, "lng": 72.5312, "phone": "+91 79 6677 0000", "image": "https://images.unsplash.com/photo-1512678080530-7760d81faba6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "SVP Hospital", "lat": 23.0232, "lng": 72.5739, "phone": "+91 79 2658 0123", "image": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "Civil Hospital, Asarwa", "lat": 23.0526, "lng": 72.6033, "phone": "+91 79 2268 3721", "image": "https://images.unsplash.com/photo-1502740479091-635887520276?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "Shalby Hospital, SG Highway", "lat": 23.0189, "lng": 72.5034, "phone": "+91 79 4020 3000", "image": "https://images.unsplash.com/photo-1538108149393-cebb47ac1136?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
    {"name": "Kiran Hospital", "lat": 23.0225, "lng": 72.5714, "phone": "+91 79 2222 3333", "image": "https://images.unsplash.com/photo-1596541223130-5d31a73fb6c6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
]

hospitals = Hospital.objects.all()

for i, h in enumerate(hospitals):
    if i < len(real_hospitals):
        h.name = real_hospitals[i]['name']
        h.latitude = real_hospitals[i]['lat']
        h.longitude = real_hospitals[i]['lng']
        h.phone = real_hospitals[i]['phone']
        h.image_url = real_hospitals[i]['image']
        h.city = "Ahmedabad"
        h.save()
        print(f"Updated {h.name} with image")

print("Hospital names and coordinates updated successfully!")
