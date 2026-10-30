// Build dependencies stay in a disposable directory, never in the plugin package.
import { execFileSync } from "node:child_process";
import { mkdtemp, readFile, writeFile, copyFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { Script } from "node:vm";

const source = dirname(fileURLToPath(import.meta.url));
const normalizeNotice = (text) => text.replace(/\r\n/g, "\n").replace(/[ \t]+$/gm, "").trim();
const temporary = await mkdtemp(join(tmpdir(), "local-translation-settings-build-"));
try {
  for (const name of ["package.json", "package-lock.json", "settings.js"]) {
    await copyFile(join(source, name), join(temporary, name));
  }
  execFileSync("npm", ["ci", "--ignore-scripts", "--no-audit", "--no-fund", "--cache", join(temporary, "npm-cache")], {
    cwd: temporary,
    stdio: "inherit",
  });
  const { build } = await import(pathToFileURL(join(temporary, "node_modules/esbuild/lib/main.js")));
  const result = await build({
    absWorkingDir: temporary,
    entryPoints: ["settings.js"],
    bundle: true,
    write: false,
    platform: "browser",
    format: "iife",
    target: "es2022",
    minify: true,
    legalComments: "inline",
    metafile: true,
  });
  const javascript = result.outputFiles[0].text.replace(/<\/script/gi, "<\\/script");
  const template = await readFile(join(source, "setup.template.html"), "utf8");
  if (template.split("<!-- SETTINGS_SCRIPT -->").length !== 2) {
    throw new Error("The settings template must contain exactly one script marker.");
  }
  // A replacement function keeps JavaScript's $&, $` and $' sequences literal.
  const html = template.replace("<!-- SETTINGS_SCRIPT -->", () => `<script>${javascript}</script>`);
  const emittedScripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  if (emittedScripts.length !== 1 || emittedScripts[0][1] !== javascript) {
    throw new Error("The emitted HTML must preserve exactly one complete inline bundle.");
  }
  // Parse the exact emitted body, without executing it, before replacing the artifact.
  new Script(emittedScripts[0][1], { filename: "setup.html inline script" });
  await writeFile(join(source, "../setup.html"), html);

  // Preserve the complete upstream licenses for every package included in the bundle.
  const packagePaths = new Set();
  for (const input of Object.keys(result.metafile.inputs)) {
    const match = input.match(/^node_modules\/((?:@[^/]+\/)?[^/]+)\//);
    if (match) packagePaths.add(match[1]);
  }
  const notices = ["# Bundled third-party software", "", "The generated ../setup.html bundles the following upstream libraries, transformed into a browser bundle by esbuild. Their complete upstream license files follow. Local Translation's settings controller and HTML template are original project code.", ""];
  for (const name of [...packagePaths].sort()) {
    const root = join(temporary, "node_modules", name);
    const metadata = JSON.parse(await readFile(join(root, "package.json"), "utf8"));
    notices.push(`## ${name} ${metadata.version}`, "");
    let license;
    for (const candidate of ["LICENSE", "LICENSE.md", "LICENSE.txt"]) {
      try {
        license = await readFile(join(root, candidate), "utf8");
        break;
      } catch (error) {
        if (error.code !== "ENOENT") throw error;
      }
    }
    if (!license) throw new Error(`Missing upstream license: ${name}`);
    notices.push("```text", normalizeNotice(license), "```", "");
    try {
      const notice = await readFile(join(root, "NOTICE"), "utf8");
      notices.push("Upstream NOTICE:", "", "```text", normalizeNotice(notice), "```", "");
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
  await writeFile(join(source, "THIRD_PARTY_NOTICES.md"), notices.join("\n"));
  console.log(`Built setup.html (${Buffer.byteLength(html)} bytes); bundled ${packagePaths.size} licensed packages.`);
} finally {
  await rm(temporary, { recursive: true, force: true });
}
