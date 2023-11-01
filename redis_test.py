import unittest
import redis_repository

class RedisTest(unittest.TestCase):
    
    def test_redis_put(self):
        redis_repository.queue_put("test", "lol")

    def test_redis_get(self):
        test = redis_repository.queue_get("test")
        self.assertEqual("lol", test)

    def test_redis_add_to_set(self):
        redis_repository.add_to_set("set", "my_value")
    
    def test_redis_contains(self):
        value = redis_repository.set_contains("set", "my_value")
        self.assertEquals(True, value)



if __name__ == '__main__':
  unittest.main()