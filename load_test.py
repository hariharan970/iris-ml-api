import asyncio
import time
import httpx

URL = "http://localhost:8000/api/v1/predict"
TOTAL_REQUESTS = 200


API_KEY = "my-secret-api-key-123"

payload = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}


async def send_request(client, request_number):
    start = time.perf_counter()

    try:
        response = await client.post(
            URL,
            json=payload,
            headers={"X-API-Key": API_KEY}
        )

        elapsed = time.perf_counter() - start

        return {
            "request": request_number,
            "status": response.status_code,
            "time": elapsed,
        }

    except Exception as e:
        return {
            "request": request_number,
            "status": "FAILED",
            "time": 0,
            "error": str(e),
        }


async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:

        start = time.perf_counter()

        tasks = [
            send_request(client, i)
            for i in range(1, TOTAL_REQUESTS + 1)
        ]

        results = await asyncio.gather(*tasks)

        total_time = time.perf_counter() - start

    successful = [
        r for r in results
        if r["status"] == 200
    ]

    failed = [
        r for r in results
        if r["status"] != 200
    ]

    response_times = [
        r["time"]
        for r in successful
    ]

    print("\n===== LOAD TEST RESULTS =====")
    print(f"Total requests:      {TOTAL_REQUESTS}")
    print(f"Successful requests: {len(successful)}")
    print(f"Failed requests:     {len(failed)}")
    print(f"Total test time:     {total_time:.3f} seconds")

    if response_times:
        print(
            f"Average response:    "
            f"{sum(response_times) / len(response_times):.3f} seconds"
        )
        print(
            f"Maximum response:    "
            f"{max(response_times):.3f} seconds"
        )
        print(
            f"Minimum response:    "
            f"{min(response_times):.3f} seconds"
        )

    if failed:
        print("\n===== FAILED REQUESTS =====")

        for result in failed:
            print(
                f"Request {result['request']}: "
                f"status={result['status']} "
                f"error={result.get('error', 'HTTP error')}"
            )


if __name__ == "__main__":
    asyncio.run(main())