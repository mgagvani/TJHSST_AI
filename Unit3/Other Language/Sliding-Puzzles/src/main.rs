// Manav Gagvani 11/9/22
// to run: cargo run -- '..\..\..\Unit1a\Sliding Puzzles\15_puzzles.txt'

use std::env;
use std::fs;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::BinaryHeap;
use std::cmp::Reverse;

use itertools::Itertools;

#[derive(Hash, Eq, PartialEq, Debug)]
struct Node {
    heuristic: u32,
    state: Vec<char>,
    depth: u32
}

#[derive(Hash, Eq, PartialEq, Debug)]
struct OrderedPair {
    i: u8, 
    j: u8
}

fn print_type<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}

fn goal_test(current: &Vec<char>, goal: &Vec<char>) -> bool {
    for (idx, value) in current.iter().enumerate() {
        if goal[idx] != value {
            false
        }
    }
    true
}

fn abs(num: i8) -> u8 {
    if num < 0 {
       let a = (-num) as u8; 
       a
    }
    else {
        let b = num as u8;
        b
    }
}

fn str_to_vec(string: &str) -> Vec<char> {
    let new_vec_full = string.chars().collect::<Vec<char>>();
    new_vec_full[2..].to_vec()
}

fn arr2mat(idx: usize, size: u8) -> OrderedPair {
    let ii = (idx as u8 / size) as u8;
    let jj = (idx as u8 % size) as u8;
    OrderedPair{i: ii, j: jj}
}

fn find_goal(puzzle: &str) -> Vec<char>{
    let s = puzzle.chars().sorted().collect::<Vec<char>>();

    let mut ss = s[3..].to_vec();

    if let Some(pos) = ss.iter().position(|x| *x == '4') {
        ss.remove(pos);
    }

    ss.push('.');

    return ss
}

fn taxicab(current: &Vec<char>, goal: &Vec<char>, size: u8) -> u32 {
    let mut goal_positions = HashMap::new();
    let mut total = 0;

        for (idx, value) in goal.iter().enumerate() {
        if *value == '.' {
            continue;
        }
        goal_positions.entry(*value).or_insert(arr2mat(idx.try_into().unwrap(), size));
    }

    for (idx, value) in current.iter().enumerate() {
        if *value == '.' {
            continue;
        }
        let goali = goal_positions.get(value).unwrap().i;
        let goalj = goal_positions.get(value).unwrap().j;
        
        let curri = arr2mat(idx, size).i;
        let currj = arr2mat(idx, size).j;

        let dy = abs(goali  as i8 - curri as i8);
        let dx = abs(goalj  as i8 - currj as i8);
        let dist = (dy + dx) as u32;
        total += dist;
    }
    
    total
}

fn astar(start: &Vec<char>, goal: &Vec<size>, size) {
    let mut closed = HashSet::new();
    let start_node = Node{taxicab(&start, &goal, size), start, 0};
    let mut fringe = BinaryHeap::new();
    fringe.push(Reverse(start_node));
    while !fringe.is_empty() {
        let v = fringe.pop();
        if goal_test(&v.state, &goal) {
            println!("result, depth: {} {}", &v.state, &v.depth);
        }
        if !closed.contains(&v.state) {
            closed.insert(&v.state);
            // TODO GET CHILDREN
        }
    }
}


/* (it doesn't work)
fn to_mat(state: &Vec<char>, size: u8) -> Vec<Vec<char>> {
    
    let mut new_vec = Vec::new();
    for i in 0..size {
        let mut _v = Vec::new();
        new_vec.push(_v);
        for j in 0..size {
            let temp = (i * size + j) as usize;
            let mut last = new_vec.last().expect("blah"); // .push(state[temp]);
            print_type(last);
            last.push(state[temp]);
        }
    }
    return new_vec;
}
*/

fn parity_check(string: &str, size: u8) -> bool {
    // let mat = to_mat(&string.chars().collect::<Vec<char>>(), size);
    let mut blankEven = false;
    let mut row = 100;
    let mut idx = 100;
    let mut numParity = 0;
    let new_vec_full = string.chars().collect::<Vec<char>>();
    let mut new_vec = new_vec_full[2..].to_vec();

    for (i, val) in new_vec.iter().enumerate() {
        if *val == '.' {
            idx = i as u8;
            row = idx / size;
            if row % 2 == 0 {
                blankEven = true;
            }
            else {
                blankEven = false;
            }
            break;
        }
    }
    // println!("row {}, idx {}", row, idx);

    // step 2 - find even/odd parity
    new_vec.remove(new_vec.iter().position(|x| *x == '.').expect(". not found"));
    // println!("without period {:?}", new_vec);
    for i in 0..new_vec.len() {
        let a = i + 1;
        for j in a..new_vec.len() {
            let left: u32 = new_vec[i].into();
            let right: u32 = new_vec[j].into();
            if left > right {
                numParity += 1;
            }
        }
    }
    // step 3 - odd/even size boards
    if size % 2 == 1 {
        if numParity % 2 == 0 {
            return true;
        }
        else {
            return false;
        }
    }
    else {
        if blankEven && numParity % 2 == 1 {
            return true;
        }
        if !blankEven && numParity & 2 == 0 {
            return false;
        }
        else {
           return true; 
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    println!("{:?}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    // println!("With text:\n{contents}");

    let lines = contents.lines(); // iterator, use .next()

    for line in lines {
        // println!("{}", line);
        let mut _chars_iter = line.chars(); // .nth(trim().parse().unwrap();
        let _char_size =  _chars_iter.next().unwrap();
        let size: u8 = _char_size as u8 - '0' as u8;
        // println!("{:?}", size);
        let goal = find_goal(line);
        // println!("goal {:?}", goal);
        let parity = parity_check(line, size);
        // println!("parity: {}", parity);
        let mut vec = str_to_vec(line);
        astar(&vec, &goal, size);
        // println!("taxicab: {}", taxicab);
    }

    // print_type(&contents);
}
