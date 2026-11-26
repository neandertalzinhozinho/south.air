//! Presets do South.air: arquivos de texto em `%APPDATA%\South.air\Presets\<nome>.sapreset`,
//! uma linha `Nome do parâmetro=valor` (valor simples, nas unidades da tabela).
//!
//! Só a tela usa isto: carregar um preset é o mesmo que mexer nos controles (cada valor passa
//! por `ParamAccess::set`, como um gesto do usuário). Nada aqui toca o motor.

use crate::param_table::{PARAMS, PARAM_COUNT};
use std::path::PathBuf;

pub const EXT: &str = "sapreset";
/// Nome do preset embutido (todos os parâmetros no padrão).
pub const DEFAULT_NAME: &str = "Default";
/// Ficam fora dos presets: delta (96) e bypass (97) são de monitoração, não de som.
pub const SKIP: [usize; 2] = [96, 97];

pub fn dir() -> Option<PathBuf> {
    std::env::var_os("APPDATA").map(|a| PathBuf::from(a).join("South.air").join("Presets"))
}

fn path(name: &str) -> Option<PathBuf> {
    dir().map(|d| d.join(format!("{name}.{EXT}")))
}

/// Nomes dos presets do usuário, em ordem alfabética (sem o embutido).
pub fn list() -> Vec<String> {
    let mut v: Vec<String> = dir()
        .and_then(|d| std::fs::read_dir(d).ok())
        .map(|rd| {
            rd.filter_map(|e| e.ok())
                .map(|e| e.path())
                .filter(|p| p.extension().and_then(|x| x.to_str()) == Some(EXT))
                .filter_map(|p| p.file_stem().and_then(|s| s.to_str()).map(str::to_string))
                .collect()
        })
        .unwrap_or_default();
    v.sort_by_key(|s| s.to_lowercase());
    v
}

/// Valores do preset embutido.
pub fn defaults() -> Vec<(usize, f64)> {
    (0..PARAM_COUNT).filter(|i| !SKIP.contains(i)).map(|i| (i, PARAMS[i].default)).collect()
}

/// Valores completos do preset `name`: parte do padrão e aplica o que o arquivo traz (nome de
/// parâmetro desconhecido é ignorado; valor fora da faixa é limitado).
pub fn load(name: &str) -> Option<Vec<(usize, f64)>> {
    if name == DEFAULT_NAME {
        return Some(defaults());
    }
    let text = std::fs::read_to_string(path(name)?).ok()?;
    let mut vals = defaults();
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let Some((k, v)) = line.rsplit_once('=') else { continue };
        let Ok(v) = v.trim().parse::<f64>() else { continue };
        if let Some(slot) = vals.iter_mut().find(|(i, _)| PARAMS[*i].name == k.trim()) {
            slot.1 = v.clamp(PARAMS[slot.0].min, PARAMS[slot.0].max);
        }
    }
    Some(vals)
}

pub fn save(name: &str, get: impl Fn(usize) -> f64) -> std::io::Result<()> {
    let d = dir().ok_or_else(|| std::io::Error::new(std::io::ErrorKind::NotFound, "APPDATA not set"))?;
    std::fs::create_dir_all(&d)?;
    let mut s = String::from("# South.air preset v1\n");
    for (i, _) in defaults() {
        s.push_str(&format!("{}={}\n", PARAMS[i].name, get(i)));
    }
    std::fs::write(d.join(format!("{name}.{EXT}")), s)
}

pub fn delete(name: &str) -> std::io::Result<()> {
    match path(name) {
        Some(p) => std::fs::remove_file(p),
        None => Ok(()),
    }
}

/// Nome válido para arquivo no Windows (sem `<>:"/\|?*`, sem espaços nas pontas, até 64
/// caracteres). Vazio = inválido.
pub fn sanitize(name: &str) -> String {
    let s: String = name.chars().filter(|c| !"<>:\"/\\|?*".contains(*c) && !c.is_control()).take(64).collect();
    let s = s.trim().trim_end_matches('.').to_string();
    if s.eq_ignore_ascii_case(DEFAULT_NAME) {
        String::new()
    } else {
        s
    }
}
