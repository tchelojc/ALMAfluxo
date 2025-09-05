import unittest
from PIL import Image
from image_processor import ImageProcessor, MAX_IMAGE_PIXELS  # Ajuste o import conforme sua estrutura

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.test_image = Image.new('RGB', (100, 100), (255, 0, 0))
    
    def test_vintage_effect(self):
        # Testar com intensidade 0
        result = ImageProcessor.apply_vintage_effect(self.test_image, 0, 0, 0)
        self.assertEqual(result.getpixel((0,0)), (255, 0, 0))
        
        # Testar com intensidade máxima
        result = ImageProcessor.apply_vintage_effect(self.test_image, 100, 0, 0)
        self.assertNotEqual(result.getpixel((0,0)), (255, 0, 0))
        
    def test_resize_large_image(self):
        large_img = Image.new('RGB', (5000, 5000))
        resized = ImageProcessor.resize_large_image(large_img)
        self.assertLess(resized.width * resized.height, MAX_IMAGE_PIXELS)

if __name__ == '__main__':
    unittest.main()