// livespec's hint under Pi: one footer line when an upgrade is waiting in this repository.
// The footer is the person's and never the model's. It runs tools/behind.py and nothing else,
// and stays out of print mode. See specs/changes/0108.
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const behind = join(dirname(dirname(fileURLToPath(import.meta.url))), "tools", "behind.py");

export default function (pi: ExtensionAPI) {
  let shown = false;
  let ended = false;
  const refresh = async (ctx: any) => {
    const result = await pi.exec("python3", [behind, "--host", "pi", "--root", ctx.cwd], { timeout: 3000 });
    if (ended) return;
    const line = result.code === 0 ? result.stdout.trim() : "";
    shown = line !== "";
    ctx.ui.setStatus("livespec", line || undefined);
  };
  pi.on("session_start", async (_event, ctx) => {
    if (!ctx.hasUI || process.env.LIVESPEC_NO_HINT) return;
    ended = false;
    await refresh(ctx);
    pi.exec("python3", [behind, "--fetch-latest"], { timeout: 5000 }).then(() => refresh(ctx), () => {});
  });
  pi.on("agent_settled", async (_event, ctx) => {
    if (shown) await refresh(ctx);
  });
  pi.on("session_shutdown", async (_event, ctx) => {
    ended = true;
    if (shown) ctx.ui.setStatus("livespec", undefined);
  });
}
