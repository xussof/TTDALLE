import os
import random
import tweepy
import requests
from os import path
from pytrends.request import TrendReq


def authenticate():
  access_token = os.environ['ACCESS_TOKEN']
  access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
  api_key = os.environ['API_KEY']
  api_key_secret = os.environ['API_KEY_SECRET']

  # Authenticate to Twitter
  auth = tweepy.OAuthHandler(api_key, api_key_secret)
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth)

  try:
    api.verify_credentials()
    print("Authentication OK")
  except:
    print("Error during authentication")
  return api


def woeid_image(WOEID, api):
  dalle_api_key = os.environ['DALLE_API_KEY']
  top_trends = api.get_place_trends(WOEID)

  country = top_trends[0]['locations'][0]['name']
  print(f"El pais o zona es: {country}")

  top_5_trends = [
    trend["name"].replace("#", "") for trend in top_trends[0]["trends"][:5]
  ]

  print(top_5_trends)

  # Unir todos los hashtags en una sola cadena de texto
  prompt = "Create an image with with random style digital art cover alike: " + ', '.join(
    top_5_trends)

  # Generar una imagen a partir de los hashtags seleccionados
  url = "https://api.openai.com/v1/images/generations"
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {dalle_api_key}"
  }
  data = {"prompt": prompt, "model": "image-alpha-001"}
  response = requests.post(url, headers=headers, json=data)
  print(response)

  # Procesar la respuesta de la API para obtener la imagen generada
  if response.status_code == 200:
    image_url = response.json()["data"][0]["url"]
    image_bytes = requests.get(image_url).content
    #Generate random number for file name
    rand_num = random.randint(0, 99999)
    file_name = f"image{rand_num}.jpg"

    #Save image to disk
    with open(file_name, "wb") as f:
      f.write(image_bytes)
      media_id = api.media_upload(file_name).media_id

    #Create a tweet with the uploaded image
    api.update_status("Todays " + country + " trending topic image #" +
                      ', #'.join(top_5_trends),
                      media_ids=[media_id])

    #Remove the image file after tweeting
    os.remove(file_name)
  else:
    print(f"Error al generar la imagen: {response.json()}")


def main():
  api = authenticate()
  #top_countries = ["1", "23424977", "23424856", "23424900", "23424846", "23424975", "23424950", "23424922", "23424747", "23424787", "23424848", "23424803", "23424829", "23424901", "23424934", "23424868", "23424775", "23424909", "23424969", "23424819", "23424853"]

  top_countries = ["23424819"]

  for country_code in top_countries:
    print(country_code)

    woeid_image(country_code, api)


if __name__ == '__main__':
  main()
