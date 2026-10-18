import { NextResponse } from "next/server";
import { getCv } from "@/lib/cvs";

export const dynamic = "force-dynamic";

/** GET /api/cvs/:id : un profil. */
export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const cv = await getCv(id);
  if (!cv) {
    return NextResponse.json({ error: `Aucun profil avec l'identifiant « ${id} ».` }, { status: 404 });
  }
  return NextResponse.json(cv);
}
