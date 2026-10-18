import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Les CV PDF sont lus sur le disque par l'API : on les embarque dans le build.
  outputFileTracingIncludes: {
    "/api/cvs/[id]/cv": ["./data/cvs/**/*"],
  },
};

export default nextConfig;
