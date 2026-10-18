"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import type { Cv } from "@/lib/cvs";
import { formatRemuneration, initials } from "@/lib/format";

type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; cv: Cv };

export default function CvDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    fetch(`/api/cvs/${encodeURIComponent(id)}`)
      .then(async (res) => {
        const body = await res.json();
        if (!res.ok) throw new Error(body.error ?? `L'API a répondu ${res.status}.`);
        return body as Cv;
      })
      .then((cv) => !cancelled && setState({ status: "ready", cv }))
      .catch((err: Error) => !cancelled && setState({ status: "error", message: err.message }));
    return () => {
      cancelled = true;
    };
  }, [id]);

  return (
    <>
      <Link href="/" className="back">
        ← Tous les profils
      </Link>

      {state.status === "loading" && <p className="lead">Chargement du profil…</p>}

      {state.status === "error" && (
        <p className="notice" role="alert">
          {state.message}
        </p>
      )}

      {state.status === "ready" && (
        <div className="detail">
          <aside className="panel">
            <span className="avatar avatar-lg" aria-hidden="true">
              {initials(state.cv.prenom, state.cv.nom)}
            </span>
            <h1 className="detail-name">
              {state.cv.prenom} <strong>{state.cv.nom}</strong>
            </h1>
            <p className="metier">{state.cv.metier}</p>
            <dl className="facts facts-col">
              <div>
                <dt>Localisation</dt>
                <dd>{state.cv.localisation}</dd>
              </div>
              <div>
                <dt>Rémunération annuelle brute</dt>
                <dd className="num">{formatRemuneration(state.cv.remuneration)}</dd>
              </div>
              <div>
                <dt>Identifiant</dt>
                <dd className="mono">{state.cv.id}</dd>
              </div>
            </dl>
            <a className="button" href={`/api/cvs/${state.cv.id}/cv`} target="_blank" rel="noopener">
              Ouvrir le PDF
            </a>
          </aside>
          <iframe
            className="pdf"
            src={`/api/cvs/${state.cv.id}/cv`}
            title={`CV de ${state.cv.prenom} ${state.cv.nom}`}
            data-testid="cv-pdf"
          />
        </div>
      )}
    </>
  );
}
