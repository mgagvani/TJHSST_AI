fn sqr(x: f64) -> f64 {
    return x * x;
}

fn factorial(n: u64) -> u64 {
    if n == 0 {
        1
    }
    else {
        n * factorial(n - 1)
    }
}

fn arrsum(values: &[i32]) -> i32 {
    let mut to_ret = 0;
    for i in 0..values.len() {
        to_ret += values[i];
    }
    to_ret
}

fn stuff() {
    let answer = 56;
    println!("Hello {}!", answer);
    for i in 0..5 {
        if i % 2 == 0 {
            println!("even {}", i);
        }
        else {
            println!("odd {}", i)
        }
    }
    let mut sum = 0.0;
    for i in 0..10 {
        sum += i as f64;
    }
    println!("sum of numbers is {}", sum);
    let a = sqr(4.0);
    println!("square is {}", a);
    let b = factorial(6);
    println!("factorial is {}", b);
    // let bigint: i64 = 0;
    let arr = [1, 3, 4, 6, 84, 43];
    let sum = arrsum(&arr);
    println!("first in arr is {}", sum);
    let mut v = Vec::new();
    v.push(16);
    v.push(20);
    v.push(30);
    let abcd = v[0];
    println!("abcd is {}", abcd);
}

fn main() {
    stuff();
}
