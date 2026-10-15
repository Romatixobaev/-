using System;
using ScottPlot;

class Program
{

    static void Main()
    {
        Console.Write("Введите а1: ");
        double a1 = double.Parse(Console.ReadLine()!);

        Console.Write("Введите b1: ");
        double b1 = double.Parse(Console.ReadLine()!);

        Console.Write("Введите а2: ");
        double a2 = double.Parse(Console.ReadLine()!);

        Console.Write("Введите b2: ");
        double b2 = double.Parse(Console.ReadLine()!);

        Console.Write("Введите а3: ");
        double a3 = double.Parse(Console.ReadLine()!);

        Console.Write("Введите b3: ");
        double b3 = double.Parse(Console.ReadLine()!);

        Console.Write("Введите x0: ");
        double x0 = double.Parse(Console.ReadLine()!);

        Console.Write("Введите xk: ");
        double xk = double.Parse(Console.ReadLine()!);

        Console.Write("Введите dx: ");
        double dx = double.Parse(Console.ReadLine()!);


        int n = (int)Math.Floor((xk - x0) / dx + 1e-10) + 1;

        double[] x = new double[n];
        double[] y = new double[n];

        Console.WriteLine("\n        x          y");
        Console.WriteLine("-------------------------");


        for (int i = 0; i < n; i++)
        {
            x[i] = x0 + i * dx;

            y[i] = a1 * Math.Sin(b1 * x[i]) + a2 * Math.Sin(b2 * x[i]) + a3 * Math.Sin(b3 * x[i]);

            Console.WriteLine($"{x[i],10:F3} {y[i],12:F6}");
        }

        Plot plot = new();
        plot.Add.Scatter(x, y);
        plot.Title("График функции y(x)");
        plot.XLabel("x");
        plot.YLabel("y");

        plot.SaveSvg("graph.svg", 800, 500);

        Console.WriteLine("\nГрафик сохранен в файле graph.svg");
    }


}