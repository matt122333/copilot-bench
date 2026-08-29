pub fn sum_of_squares(n: i64) -> i64 {
    (1..=n).map(|i| i * i).sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sumsq() {
        assert_eq!(sum_of_squares(4), 30);
    }
}

fn main() {
    println!("{}", sum_of_squares(4));
}
