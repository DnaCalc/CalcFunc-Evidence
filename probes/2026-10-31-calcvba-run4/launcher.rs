use calc_oracle_excel::{ReportedExcel, Worker, run_isolated};
use std::{ffi::OsString, path::PathBuf, time::Duration};

fn main() {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    assert_eq!(args.len(), 1, "pass the prepared worker directory");
    let dir = std::path::absolute(PathBuf::from(&args[0])).unwrap();
    let run = run_isolated(&Worker {
        program: PathBuf::from(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"),
        args: ["-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File"]
            .into_iter().map(OsString::from)
            .chain([dir.join("witness-worker.ps1").into_os_string(), "-Request".into(),
                dir.join("request.json").into_os_string(), "-Result".into(),
                dir.join("result.json").into_os_string()]).collect(),
        dir: dir.clone(),
        timeout: Duration::from_secs(180),
        exit_grace: Duration::from_secs(15),
        excel_image: "EXCEL.EXE".into(),
    });
    std::fs::write(dir.join("isolation.txt"), format!("{run:#?}\n")).unwrap();
    let run = run.expect("isolated worker failed");
    println!("{run:#?}");
    assert_eq!(run.exit_code, Some(0));
    assert!(run.done);
    assert!(matches!(run.excel, ReportedExcel::Exited | ReportedExcel::Gone));
    assert!(run.stderr.is_empty());
}
