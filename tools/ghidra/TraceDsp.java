// Ghidra 12.x script: trace the DSP call graph from a root RVA and write the
// decompiled C of each reachable function to docs/engine/decomp/.
// Usage: -postScript TraceDsp.java 0x350F20 2
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import java.io.File;
import java.io.PrintWriter;
import java.util.*;

public class TraceDsp extends GhidraScript {
    DecompInterface ifc;
    File outDir;
    Set<Long> seen = new HashSet<>();
    PrintWriter graph;

    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        long off = Long.parseLong(a[0].replace("0x", "").replace("0X", ""), 16);
        int maxDepth = a.length > 1 ? Integer.parseInt(a[1]) : 1;
        long base = currentProgram.getImageBase().getOffset();
        Address addr = currentProgram.getAddressFactory().getDefaultAddressSpace()
                .getAddress(off >= base ? off : base + off);
        Function root = getFunctionAt(addr);
        if (root == null) root = getFunctionContaining(addr);
        if (root == null) { println("root not found"); return; }

        outDir = new File("D:/PROJETOS/soultree/docs/engine/decomp");
        outDir.mkdirs();
        graph = new PrintWriter(new File(outDir, "callgraph.txt"), "UTF-8");

        ifc = new DecompInterface();
        ifc.toggleCCode(true);
        ifc.toggleSyntaxTree(true);
        ifc.openProgram(currentProgram);

        graph.println("# root " + root.getName() + " @ 0x" + Long.toHexString(root.getEntryPoint().getOffset()));
        walk(root, 0, maxDepth);
        graph.close();
        ifc.dispose();
        println("wrote " + seen.size() + " functions to " + outDir.getAbsolutePath());
    }

    void walk(Function f, int depth, int maxDepth) {
        long ep = f.getEntryPoint().getOffset();
        if (!seen.add(ep)) return;
        String name = f.getName();
        graph.println("  ".repeat(depth) + "0x" + Long.toHexString(ep) + " " + name
                + " size=" + f.getBody().getNumAddresses());
        try {
            DecompileResults res = ifc.decompileFunction(f, 120, monitor);
            if (res.decompileCompleted()) {
                String fn = String.format("%08X_%s.c", ep, name.replaceAll("[^A-Za-z0-9_.-]", "_"));
                try (PrintWriter w = new PrintWriter(new File(outDir, fn), "UTF-8")) {
                    w.println("// " + name + " @ 0x" + Long.toHexString(ep));
                    w.println(res.getDecompiledFunction().getC());
                }
            }
        } catch (Exception e) {
            graph.println("  ".repeat(depth) + "  ! " + e.getMessage());
        }
        if (depth >= maxDepth) return;
        try {
            for (Function c : f.getCalledFunctions(monitor)) {
                walk(c, depth + 1, maxDepth);
            }
        } catch (Exception e) {
            graph.println("  ".repeat(depth) + "  ! callees: " + e.getMessage());
        }
    }
}
