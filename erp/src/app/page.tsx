"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import type { Cv } from "@/lib/cvs";
import { formatRemuneration, initials } from "@/lib/format";

type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; cvs: Cv[] };

export default function CvListPage() {
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    fetch("/api/cvs")
      .then((res) => {
        if (!res.ok) throw new Error(`L'API a répondu ${res.status}.`);
        return res.json() as Promise<{ total: number; cvs: Cv[] }>;
      })
      .then((data) => !cancelled && setState({ status: "ready", cvs: data.cvs }))
      .catch((err: Error) => !cancelled && setState({ status: "error", message: err.message }));
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <>
      <section className="page-head">
        <p className="eyebrow">CVthèque</p>
        <h1>Tous les profils</h1>
        <p className="lead" data-testid="cv-count">
          {state.status === "ready"
            ? `${state.cvs.length} profils disponibles. Ouvrez une fiche pour consulter le CV.`
            : "Chargement des profils…"}
        </p>
      </section>

      {state.status === "error" && (
        <p className="notice" role="alert">
          Impossible de charger les profils : {state.message} Vérifiez que le serveur tourne, puis rechargez la page.
        </p>
      )}

      {state.status === "loading" && (
        <ul className="grid" aria-hidden="true">
          {Array.from({ length: 6 }, (_, i) => (
            <li key={i} className="card skeleton" />
          ))}
        </ul>
      )}

      {state.status === "ready" && state.cvs.length === 0 && (
        <p className="notice">La CVthèque est vide. Ajoutez des profils dans data/cvs.json.</p>
      )}

      {state.status === "ready" && state.cvs.length > 0 && (
        <ul className="grid">
          {state.cvs.map((cv) => (
            <li key={cv.id}>
              <Link href={`/cvs/${cv.id}`} className="card" data-testid="cv-card">
                <div className="card-top">
                  <span className="avatar" aria-hidden="true">{initials(cv.prenom, cv.nom)}</span>
                  <div className="who">
                    <h2>
                      {cv.prenom} <strong>{cv.nom}</strong>
                    </h2>
                    <p className="metier">{cv.metier}</p>
                  </div>
                </div>
                <dl className="facts">
                  <div>
                    <dt>Localisation</dt>
                    <dd>{cv.localisation}</dd>
                  </div>
                  <div>
                    <dt>Rémunération</dt>
                    <dd className="num">{formatRemuneration(cv.remuneration)}</dd>
                  </div>
                </dl>
                <span className="card-cta">Voir la fiche →</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
