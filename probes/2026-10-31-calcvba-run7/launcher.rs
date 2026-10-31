use calc_oracle_excel::{ReportedExcel, WitnessCall, WitnessRequest, read_witnesses};
use std::{path::PathBuf, time::Duration};

fn main() {
    let folder = PathBuf::from(std::env::args_os().nth(1).expect("pass the evidence run folder"));
    let input: serde_json::Value = serde_json::from_slice(&std::fs::read(folder.join("requests.json")).unwrap()).unwrap();
    assert_eq!(input["function"], "POISSON.DIST");
    let rows = input["witnesses"].as_array().unwrap();
    assert_eq!(rows.len(), 38);
    let calls = rows.iter().map(|row| WitnessCall {
        id: row["id"].as_str().unwrap().into(),
        args: row["args"].as_array().unwrap().iter().enumerate()
            .map(|(i, value)| calc_verdict::decode_argument(value, &format!("args[{i}]")).unwrap()).collect(),
        result_index: None,
    }).collect();
    let outcome = read_witnesses(&WitnessRequest {
        function: "POISSON.DIST".into(), calls,
        work_dir: folder.join("poisson-dist"), timeout: Duration::from_secs(180),
    }).expect("witness reading failed");
    std::fs::write(folder.join("isolation.txt"), format!("{:#?}\n", outcome.run)).unwrap();
    assert_eq!(outcome.run.exit_code, Some(0));
    assert!(outcome.run.done && outcome.run.stderr.is_empty());
    assert!(matches!(outcome.run.excel, ReportedExcel::Exited | ReportedExcel::Gone));
    assert_eq!(outcome.readings.len(), 38);
    for row in &outcome.readings { assert!(row.value.is_ok(), "{}: {:?}", row.id, row.value); }
    println!("{} readings; environment: {:#?}; run: {:#?}", outcome.readings.len(), outcome.environment, outcome.run);
}
