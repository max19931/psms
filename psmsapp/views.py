from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import ( generics, status)
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from datetime import date

from .models import *
from .serializers import ( CameraDetailSerializer, CameraTypesSerializer )


### show camera details
class CameraDetailView(generics.ListAPIView):
  queryset = CameraDetail.objects.all()
  serializer_class = CameraDetailSerializer

  def list(self, request):
    queryset = self.get_queryset()
    serializer = CameraDetailSerializer(queryset, many = True)
    return Response(serializer.data)


class CreateListCameraDetailView(generics.ListCreateAPIView):
  queryset = CameraDetail.objects.all()
  serializer_class = CameraDetailSerializer

  def post(self, request, format=None):
    camera_type = CameraTypes.objects.get(id=request.data['camera_type'])

    cameradetail = CameraDetail.objects.create(
                  name = request.data['name'],
                  model = request.data['model'],
                  p_serial_number = request.data['p_serial_number'],
                  status = request.data['status'],
                  camera_type= camera_type)
    return Response(status=status.HTTP_201_CREATED)

  def list(self, request):
    queryset = self.get_queryset()
    serializer = CameraDetailSerializer(queryset, many = True)
    return Response(serializer.data)

class UpCameraDetailView(generics.RetrieveUpdateAPIView):
  queryset = CameraDetail.objects.all()
  serializer_class = CameraDetailSerializer

  def put(self, request, pk, format=None):
      try:
          updated_camera = CameraDetail.objects.get(pk=pk)
          serializer = CameraDetailSerializer(
              updated_camera, data=request.data)
          if serializer.is_valid():
              serializer.save()
          else:
              return Response({"response": "data not valid"})
          return Response(serializer.data)
      except Exception as e:
          raise e

class DelCameraDetailView(generics.RetrieveDestroyAPIView):
  queryset = CameraDetail.objects.all()
  serializer_class = CameraDetailSerializer

  def delete(self, request, pk, format=None):
      try:
          updated_camera = CameraDetail.objects.get(pk=pk)
          updated_camera.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
      except Exception as e:
          raise e


#### create camera details
class AddCameraDetailView(generics.ListCreateAPIView):
  queryset = CameraDetail.objects.all()
  serializer_class = CameraDetailSerializer
  def post(self, request, format=None):
    camera_type = CameraTypes.objects.get(id=request.data['camera_type'])

    cameradetail = CameraDetail.objects.create(
                  name = request.data['name'],
                  model = request.data['model'],
                  p_serial_number = request.data['p_serial_number'],
                  status = request.data['status'],
                  camera_type= camera_type)
    return Response(status=status.HTTP_201_CREATED)



### show types of cameras
class CameraTypeView(generics.ListAPIView):
  queryset = CameraTypes.objects.all()
  serializer_class = CameraTypesSerializer

  def list(self, request):
    queryset = self.get_queryset()
    serializer = CameraTypesSerializer(queryset, many=True)
    return Response(serializer.data)



### create new type of camera
class NewCameraType(generics.CreateAPIView):
  queryset = CameraTypes.objects.all()
  serializer_class = CameraTypesSerializer
  
  def post(self, request):
    cameratype = CameraTypes.objects.create(name = request.data['name'])
    return Response(status=status.HTTP_201_CREATED)

### delete type of camera
class DelCameraType(generics.RetrieveDestroyAPIView):
  queryset = CameraTypes.objects.all()
  serializer_class = CameraTypesSerializer

  def delete(self, request, pk, format=None):
      try:
          updated_camera_type = CameraTypes.objects.get(pk=pk)
          updated_camera_type.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
      except Exception as e:
          raise e


# ya keegan
class AddCameraType(generics.CreateAPIView):
    serializer_class = CameraTypesSerializer
    queryset = CameraTypes.objects.all()

    def post(self, request, format=None):
        cameradetail = request.data.pop('cameradetail')
        try:
            camera_type = CameraTypes.objects.create(
              name=request.data['name'])

            for item in cameradetail:
                CameraDetail.objects.create(
                  camera_type=camera_type,
                  status = item['status'],
                  name = item['name'],
                  model = item['model'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

class chartView(generics.ListAPIView):
  queryset = CameraDetail.objects.filter(status="Bad")
  # queryset2 = CameraDetail.objects.filter(status="Fair")
  # queryset3 = CameraDetail.objects.filter(status="Bad")
  serializer_class = CameraDetailSerializer

  def list(self, request):
    queryset = self.get_queryset()
    serializer = CameraTypesSerializer(queryset, many=True)
    return Response(serializer.data)





# {
# "cameradetail":[{
#     "name": "infinix",
#     "model": "cannon",
#     "status": null,
#     "camera_type": null
# },{
#     "name": "Kodak",
#     "model": "4567",
#     "status": null,
#     "camera_type": null
# }],
#     "name": "HD"
# }