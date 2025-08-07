from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

class RedisRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 1000
        self.rate_limit_duration = 300
        self.block_duration = 120
        self.block_allowance = 2

    def __call__(self, request):
        # اگر ریت لیمیت غیرفعال است، مستقیم ادامه بده
        if not getattr(settings, 'RATE_LIMIT_ENABLED', False):
            return self.get_response(request)

        ip = self.get_ip_address(request)
        count_key = f"rate_limit:{ip}"
        block_key = f"block:{ip}"

        block_data = cache.get(block_key)
        if block_data:
            block_count = block_data.get('count', 0)
            if block_count >= self.block_allowance:
                return JsonResponse(
                    {"error": "شما به مدت 2 دقیقه مسدود شده‌اید. لطفاً بعداً تلاش کنید."},
                    status=429
                )
            else:
                block_data['count'] = block_count + 1
                cache.set(block_key, block_data, timeout=self.block_duration)
                return self.get_response(request)

        count = cache.get(count_key)
        if count is None:
            cache.set(count_key, 1, timeout=self.rate_limit_duration)
        elif count >= self.rate_limit:
            cache.set(block_key, {'count': 1}, timeout=self.block_duration)
            return JsonResponse(
                {"error": "تعداد درخواست‌های شما بیش از حد مجاز است. شما به مدت 2 دقیقه مسدود شده‌اید."},
                status=429
            )
        else:
            cache.incr(count_key)

        return self.get_response(request)

    def get_ip_address(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
