
using System;
using System.Collections.Generic;
using System.IO;

class Program
{
    static void Main()
    {
        // Вводим коэффициенты функции
        Console.WriteLine("\nРасчет функции y(x)");
        Console.WriteLine("y = a1*sin(b1*x) + a2*sin(b2*x) + a3*sin(b3*x)\n");

        double a1 = 0, b1 = 0, a2 = 0,b2 = 0, a3 = 0,b3 = 0,
        x0 = 0, xk = 0,dx = 0;

        try
        {
        //ввод начальных данных
        Console.Write("Введите a1: ");
         a1 = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите b1: ");
         b1 = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите a2: ");
         a2 = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите b2: ");
         b2 = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите a3: ");
         a3 = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите b3: ");
         b3 = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите начальное значение x0: ");
         x0 = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите конечное значение xk: ");
         xk = Convert.ToDouble(Console.ReadLine());

        Console.Write("Введите шаг dx: ");
         dx = Convert.ToDouble(Console.ReadLine());
        ////
        }
        catch (Exception)
        {
         Console.WriteLine("\nНекорректный ввод начальных данных!\n");   
         return;
        }
       
        // проверка зачений для x
        if (dx <= 0 || xk < x0)
        {
            Console.WriteLine("\nНекорректный ввод! Проверьте x0, xk и dx.\n");
            return;
        }

        // списки для хранения x и y
        List<double> xValues = new List<double>();
        List<double> yValues = new List<double>();

        // перебор значения x от x0 до xk с шагом dx
        for (double x = x0; x <= xk; x += dx)
        {
            // вычисляем значение функции
            double y = a1 * Math.Sin(b1 * x)
                     + a2 * Math.Sin(b2 * x)
                     + a3 * Math.Sin(b3 * x);

            // сохраняем значения
            xValues.Add(x);
            yValues.Add(y);
        }

        // выводим значения
        Console.WriteLine();
        Console.WriteLine("       x       |       y");
        Console.WriteLine("-----------------------------");

        for (int i = 0; i < xValues.Count; i++)
        {
          Console.WriteLine(xValues[i] + " | " + yValues[i]);
        }

        //min и max значение y
        double minY = yValues[0];
        double maxY = yValues[0];

        //находим min и max по y
        for (int i = 0; i < yValues.Count; i++)
        {
            if (yValues[i] < minY)
                minY = yValues[i];

            if (yValues[i] > maxY)
                maxY = yValues[i];
        }

        // отступ сверху и снизу графика
        double otstup = (maxY - minY) * 0.1;
        minY = minY - otstup;
        maxY = maxY + otstup;

        // размер изображения
        int width = 800;
        int height = 500;
        int margin = 50;

        // текст SVG-файла
        string svg = "";

        svg += "<svg xmlns='http://www.w3.org/2000/svg' ";
        svg += "width='800' height='500'>";

        // фон
        svg += "<rect width='100%' height='100%' fill='white'/>";

        // заголовок графика
        svg += "<text x='400' y='25' text-anchor='middle' ";
        svg += "font-size='18'>График функции y(x)</text>";

        // оси координат
        double zeroX = margin;
        double zeroY = height - margin;

        // ось X
        svg += $"<line x1='{margin}' y1='{zeroY}' ";
        svg += $"x2='{width - margin}' y2='{zeroY}' ";
        svg += "stroke='black'/>";

        // ось Y
        svg += $"<line x1='{zeroX}' y1='{margin}' ";
        svg += $"x2='{zeroX}' y2='{height - margin}' ";
        svg += "stroke='black'/>";

        // подписываем оси
        svg += $"<text x='{width - margin}' y='{zeroY - 10}'>X</text>";
        svg += $"<text x='{zeroX + 10}' y='{margin}'>Y</text>";

        // график по рассчитанным точкам
        svg += "<polyline fill='none' stroke='blue' stroke-width='2' points='";

        for (int i = 0; i < xValues.Count; i++)
        {
            // переводим значение x в координату изображения
            double px = margin
                + (xValues[i] - x0) / (xk - x0)
                * (width - 2 * margin);

            // переводим значение y в координату изображения
            double py = height - margin
                - (yValues[i] - minY) / (maxY - minY)
                * (height - 2 * margin);

            // добавляем точку в график
            svg += $"{px.ToString(System.Globalization.CultureInfo.InvariantCulture)},";
            svg += $"{py.ToString(System.Globalization.CultureInfo.InvariantCulture)} ";
        }

        svg += "'/>";
        svg += "</svg>";

        // сохраняем график в файл
        File.WriteAllText("graph.svg", svg);

        Console.WriteLine();
        Console.WriteLine("График сохранен в файле graph.svg");
    }
}
