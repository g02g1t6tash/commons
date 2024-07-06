Here's an overview of LINQ in C# with code examples demonstrating various LINQ concepts and operations:

## Introduction to LINQ

LINQ (Language Integrated Query) is a powerful feature in C# that allows you to query and manipulate data from various sources using a consistent syntax. It can work with in-memory collections, databases, XML, and more.

## Basic LINQ Query

Let's start with a simple LINQ query:

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

        var evenNumbers = from num in numbers
                          where num % 2 == 0
                          select num;

        Console.WriteLine("Even numbers:");
        foreach (var num in evenNumbers)
        {
            Console.WriteLine(num);
        }
    }
}
```

This query selects even numbers from the list.

## LINQ Operators

LINQ provides many operators for querying and transforming data. Here are some common ones:

### Where

```csharp
var adults = people.Where(p => p.Age >= 18);
```

### Select

```csharp
var names = people.Select(p => p.Name);
```

### OrderBy

```csharp
var sortedPeople = people.OrderBy(p => p.Age);
```

### GroupBy

```csharp
var groupedPeople = people.GroupBy(p => p.City);
```

## Advanced LINQ Operations

### Join

Joining two collections:

```csharp
var query = from c in customers
            join o in orders on c.CustomerID equals o.CustomerID
            select new { c.Name, o.OrderID };
```

### SelectMany

Flattening nested collections:

```csharp
var allOrders = customers.SelectMany(c => c.Orders);
```

### Aggregate Functions

```csharp
int sum = numbers.Sum();
double average = numbers.Average();
int max = numbers.Max();
```

### Deferred Execution

LINQ uses deferred execution, meaning the query is not executed until the results are actually used:

```csharp
var query = numbers.Where(n => n > 5);
numbers.Add(11); // This will be included in the results
foreach (var num in query)
{
    Console.WriteLine(num);
}
```

### Immediate Execution

You can force immediate execution using methods like ToList(), ToArray(), or Count():

```csharp
var immediateResult = numbers.Where(n => n > 5).ToList();
```

## Complete Example

Here's a more comprehensive example demonstrating various LINQ features:

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

class Program
{
    class Person
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public string City { get; set; }
    }

    static void Main()
    {
        List<Person> people = new List<Person>
        {
            new Person { Name = "Alice", Age = 25, City = "New York" },
            new Person { Name = "Bob", Age = 30, City = "London" },
            new Person { Name = "Charlie", Age = 35, City = "Paris" },
            new Person { Name = "David", Age = 28, City = "London" },
            new Person { Name = "Eve", Age = 22, City = "New York" }
        };

        // Query syntax
        var youngPeople = from p in people
                          where p.Age < 30
                          orderby p.Name
                          select new { p.Name, p.Age };

        Console.WriteLine("Young people (Age < 30):");
        foreach (var person in youngPeople)
        {
            Console.WriteLine($"{person.Name}: {person.Age}");
        }

        // Method syntax
        var cityCounts = people.GroupBy(p => p.City)
                               .Select(g => new { City = g.Key, Count = g.Count() })
                               .OrderByDescending(x => x.Count);

        Console.WriteLine("\nPeople count by city:");
        foreach (var cityCount in cityCounts)
        {
            Console.WriteLine($"{cityCount.City}: {cityCount.Count}");
        }

        // Aggregate functions
        double averageAge = people.Average(p => p.Age);
        Console.WriteLine($"\nAverage age: {averageAge:F1}");

        // First or default
        var firstNewYorker = people.FirstOrDefault(p => p.City == "New York");
        Console.WriteLine($"\nFirst person from New York: {firstNewYorker?.Name ?? "None"}");
    }
}
```

This example demonstrates various LINQ concepts including query syntax, method syntax, filtering, ordering, grouping, projections, and aggregate functions.

LINQ provides a powerful and expressive way to work with data in C#, allowing you to write complex queries with minimal code.

Citations:
[1] https://learn.microsoft.com/en-us/dotnet/csharp/linq/get-started/introduction-to-linq-queries
[2] https://learn.microsoft.com/lt-lt/dotnet/csharp/linq/get-started/write-linq-queries
[3] https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/
[4] https://code-maze.com/advanced-linq/
[5] https://www.tutorialsteacher.com/linq/sample-linq-queries
[6] https://www.tutorialspoint.com/linq/linq_query_operators.htm
[7] https://www.youtube.com/watch?v=5l2qA3Pc83M
[8] https://www.c-sharpcorner.com/UploadFile/72d20e/concept-of-linq-with-C-Sharp/
[9] https://blexin.com/en/blog-en/linq-in-depth-advanced-features/
[10] https://www.tutorialsteacher.com/linq/linq-standard-query-operators
[11] https://efficientuser.com/2023/05/09/advanced-linq-query-techniques-in-c-with-code-samples/