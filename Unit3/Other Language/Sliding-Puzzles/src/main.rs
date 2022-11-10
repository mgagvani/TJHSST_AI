// Manav Gagvani 11/9/22
// to run: cargo run -- '..\..\..\Unit1a\Sliding Puzzles\15_puzzles.txt'

use std::env;
use std::fs;

fn print_type<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    println!("{:?}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    println!("With text:\n{contents}");

    let mut lines = contents.lines(); // iterator, use .next()

    for line in lines {
        println!("{}", line);
        println!("epic gamer moment");
    }

    // print_type(&contents);
}
