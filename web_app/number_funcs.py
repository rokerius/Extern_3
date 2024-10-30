# Проверяет, правильно ли определены долгота и широта.
def is_valid_coordinates(latitude, longitude):
    if isinstance(latitude, (int, float)) and isinstance(longitude, (int, float)):
        if -90 <= latitude <= 90 and -180 <= longitude <= 180:
            return True
    return False
