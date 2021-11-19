def parse_data(data):
  data = data['main']
  del data['humidity']
  del data['pressure']
  return data