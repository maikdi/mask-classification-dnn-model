# Mask or No Mask DNN Classification Model

## Description

These are the files necessary needed to deploy a DNN model into a website via heroku. Also includes a DNN model used to classify whether the subject face is a mask wearer vs non mask wearer.

#

## Sekilas mengenai input model

Basic Requirements for the model to work

- Support Image files are any formats that are supported by cv2.imread() of OpenCV 4.2.0 (.jpeg, .jp2, .bmp, .dib, .jpg, etc.)

#

## Model details

The model is saved with file name "Mask Classification Model_1.npy" (yes i used .npy because the saved model is just a dictionary filled with the Neural Network Parameters and is easiest done with .npy)

## How to run 

1. Pastikan Anda sudah menginstall Anaconda.
1. Buka terminal/command prompt/power shell.
1. Buat virtual environment dengan\
   `conda create -n <nama-environment> python=3.9`
1. Aktifkan virtual environment dengan\
   `conda activate <nama-environment>`
1. Install semua dependency/package Python dengan\
   `pip install -r requirements.txt`
1. Jalankan API menggunakan perintah\
   `python app.py`

## Akses melalui Website

1. Anda akan diberikan URL untuk membuka website berupa `localhost:5000/` atau `127.0.0.1:5000/`.
1. Buka URL dengan browser, coba masukkan gambar kucing atau anjing yang ingin di prediksi.
1. Anda akan diberikan prediksi bahwa pada gambar tersebut terdapat kucing atau anjing pada halaman website.
