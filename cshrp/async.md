Here's a comprehensive example demonstrating asynchronous programming in C# using async/await, Task.Run(), best practices, and cancellation:

```csharp
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static readonly HttpClient s_client = new HttpClient();
    static readonly List<string> s_urlList = new List<string>
    {
        "https://learn.microsoft.com",
        "https://learn.microsoft.com/aspnet/core",
        "https://learn.microsoft.com/azure",
        "https://learn.microsoft.com/dotnet"
    };

    static async Task Main(string[] args)
    {
        Console.WriteLine("Asynchronous Programming Example");

        try
        {
            await RunAsyncOperationsAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }

        Console.WriteLine("Press any key to exit...");
        Console.ReadKey();
    }

    static async Task RunAsyncOperationsAsync()
    {
        using var cts = new CancellationTokenSource();
        cts.CancelAfter(TimeSpan.FromSeconds(5)); // Cancel after 5 seconds

        try
        {
            var downloadTask = DownloadUrlsAsync(cts.Token);
            var cpuBoundTask = PerformCpuBoundOperationAsync(cts.Token);

            await Task.WhenAll(downloadTask, cpuBoundTask);

            Console.WriteLine($"Total bytes downloaded: {await downloadTask}");
            Console.WriteLine($"CPU-bound operation result: {await cpuBoundTask}");
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Operation was cancelled.");
        }
    }

    static async Task<long> DownloadUrlsAsync(CancellationToken cancellationToken)
    {
        long totalBytes = 0;

        foreach (var url in s_urlList)
        {
            try
            {
                var result = await DownloadUrlAsync(url, cancellationToken);
                totalBytes += result;
                Console.WriteLine($"Downloaded {result} bytes from {url}");
            }
            catch (Exception ex) when (ex is not OperationCanceledException)
            {
                Console.WriteLine($"Error downloading {url}: {ex.Message}");
            }
        }

        return totalBytes;
    }

    static async Task<int> DownloadUrlAsync(string url, CancellationToken cancellationToken)
    {
        // Use ConfigureAwait(false) when you don't need to return to the original context
        var response = await s_client.GetAsync(url, cancellationToken).ConfigureAwait(false);
        var content = await response.Content.ReadAsByteArrayAsync(cancellationToken).ConfigureAwait(false);
        return content.Length;
    }

    static Task<int> PerformCpuBoundOperationAsync(CancellationToken cancellationToken)
    {
        // Use Task.Run for CPU-bound operations
        return Task.Run(() =>
        {
            int result = 0;
            for (int i = 0; i < 1000000; i++)
            {
                cancellationToken.ThrowIfCancellationRequested();
                result += i;
            }
            return result;
        }, cancellationToken);
    }
}
```

This example demonstrates:

1. **Asynchronous Programming with async/await**:
   - The `Main` method is marked as `async Task` to allow the use of `await`.
   - Asynchronous methods are defined using the `async` keyword and return `Task` or `Task<T>`.

2. **Introduction to async/await and Task**:
   - `DownloadUrlsAsync` and `DownloadUrlAsync` methods use `async/await` for I/O-bound operations.
   - `Task.WhenAll` is used to run multiple tasks concurrently.

3. **Using Task.Run()**:
   - `PerformCpuBoundOperationAsync` uses `Task.Run` to offload CPU-bound work to a background thread.

4. **Best practices in asynchronous programming**:
   - Avoiding `async void` (except for event handlers).
   - Using `ConfigureAwait(false)` when context is not needed.
   - Proper exception handling with `try/catch` blocks.
   - Returning `Task` or `Task<T>` from async methods.

5. **Cancelling asynchronous operations**:
   - A `CancellationTokenSource` is used to create a cancellation token.
   - The token is passed to async methods to support cancellation.
   - `CancelAfter` is used to automatically cancel after a timeout.
   - `ThrowIfCancellationRequested` is called in the CPU-bound operation to check for cancellation.

This code provides a comprehensive example of asynchronous programming in C#, incorporating best practices and demonstrating how to handle both I/O-bound and CPU-bound operations asynchronously[1][2][3][4][5].

Citations:
[1] https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/?WT.mc_id=DT-MVP-5003235
[2] https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios
[3] https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming?WT.mc_id=DT-MVP-5000058
[4] https://johnthiriet.com/cancel-asynchronous-operation-in-csharp/
[5] https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/cancel-async-tasks-after-a-period-of-time