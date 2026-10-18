import { readFile } from "node:fs/promises";
import path from "node:path";

/** Un profil de la CVthèque, tel qu'il est stocké dans data/cvs.json. */
export type Cv = {
  id: string;
  prenom: string;
  nom: string;
  localisation: string;
  metier: string;
  /** Rémunération annuelle brute, en euros. */
  remuneration: number;
  /** Chemin du PDF, relatif au dossier data/ (ex. "cvs/cv-001-lea-martin.pdf"). */
  cv: string;
};

const DATA_DIR = path.join(process.cwd(), "data");
const DB_FILE = path.join(DATA_DIR, "cvs.json");
const CV_DIR = path.join(DATA_DIR, "cvs");

/** Lit la base locale à chaque appel : une modification du fichier est visible sans redémarrer. */
export async function listCvs(): Promise<Cv[]> {
  const raw = await readFile(DB_FILE, "utf-8");
  return JSON.parse(raw) as Cv[];
}

export async function getCv(id: string): Promise<Cv | undefined> {
  const cvs = await listCvs();
  return cvs.find((cv) => cv.id === id);
}

/** Renvoie le chemin absolu du PDF, en refusant tout chemin qui sortirait de data/cvs. */
export function resolveCvFile(cv: Cv): string | null {
  const file = path.resolve(DATA_DIR, cv.cv);
  return file.startsWith(CV_DIR + path.sep) ? file : null;
}
