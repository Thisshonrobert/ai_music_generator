from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
import magenta.music as mm
from magenta.models.music_vae import TrainedModel
from magenta.music.protobuf import music_pb2
import tarfile

class ProcessImageView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image_features = self.process_image(image_file)
            music_sequence = self.generate_music(image_features)
            return render(request, self.template_name, {'music_sequence': music_sequence})
        return render(request, self.template_name)

    def process_image(self, image_file):
        image_path = default_storage.save('uploaded_images/' + image_file.name, ContentFile(image_file.read()))
        image_path = settings.MEDIA_ROOT + '/' + image_path

        # Load the image and preprocess it for the InceptionV3 model
        img = Image.open(image_path)
        img = img.resize((299, 299))  # InceptionV3 input size
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Load pre-trained InceptionV3 model
        inception_model = InceptionV3(weights='imagenet', include_top=False)

        # Get features from the pre-trained model
        image_features = inception_model.predict(img_array).flatten()

        return image_features

    def generate_music(self, image_features):
        # Extract the MusicVAE model from the tar file
        tar_file_path = 'C:\projects\django_projects\music_generator_ai\music_generator_ai\models\musicvae\hierdec-trio_16bar.tar'
        extracted_model_path = 'C:\projects\django_projects\music_generator_ai\music_generator_ai\models\musicvae'

        with tarfile.open(tar_file_path, 'r') as tar:
            tar.extractall(path=extracted_model_path)

        # Load the MusicVAE model
        model_path = extracted_model_path + '/music_vae_model.ckpt'
        model = TrainedModel(model_path)

        # Generate music
        z = model.encode([image_features])
        generated_sequence = model.decode(z, length=64)

        # Convert to MIDI
        midi_file = 'generated_music.mid'
        mm.sequence_proto_to_midi_file(generated_sequence, midi_file)

        return midi_file
