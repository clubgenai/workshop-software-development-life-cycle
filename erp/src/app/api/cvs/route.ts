import { NextResponse } from "next/server";
import { listCvs } from "@/lib/cvs";

export const dynamic = "force-dynamic";

/** GET /api/cvs : tous les profils de la CVthèque. */
export async function GET() {
  const cvs = await listCvs();
  return NextResponse.json({ total: cvs.length, cvs });
}
