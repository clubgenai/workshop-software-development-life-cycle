import { readFile } from "node:fs/promises";
import { NextResponse } from "next/server";
import { getCv, resolveCvFile } from "@/lib/cvs";

export const dynamic = "force-dynamic";

/** GET /api/cvs/:id/cv : le CV au format PDF, affiché dans le navigateur. */
export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const cv = await getCv(id);
  const file = cv ? resolveCvFile(cv) : null;
  if (!cv || !file) {
    return NextResponse.json({ error: `Aucun CV pour l'identifiant « ${id} ».` }, { status: 404 });
  }
  try {
    const pdf = await readFile(file);
    return new Response(new Uint8Array(pdf), {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `inline; filename="${file.split(/[\\/]/).pop()}"`,
      },
    });
  } catch {
    return NextResponse.json({ error: `Le fichier du CV « ${id} » est introuvable sur le disque.` }, { status: 404 });
  }
}
