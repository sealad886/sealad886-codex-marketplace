pub fn greet() -> &'static str { "Hello" }
#[test]
fn greeting() { assert_eq!(greet(), "Hello"); }
