// Ghidra 12.x script: decompile RVAs to docs/engine/decomp/<addr>.c and print a
// one-line summary (signature + first lines) for each.
// Usage: -postScript DecompileToFiles.java 0x353510 0x354F90 ...
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.File;
import java.io.PrintWriter;

public class DecompileToFiles extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        long base = currentProgram.getImageBase().getOffset();
        File dir = new File("D:/PROJETOS/soultree/docs/engine/decomp");
        dir.mkdirs();
        DecompInterface ifc = new DecompInterface();
        ifc.toggleCCode(true);
        ifc.toggleSyntaxTree(true);
        ifc.openProgram(currentProgram);

        for (String a : args) {
            long off = Long.parseLong(a.replace("0x", "").replace("0X", ""), 16);
            long va = (off >= base) ? off : base + off;
            Address addr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(va);
            Function f = getFunctionAt(addr);
            if (f == null) f = getFunctionContaining(addr);
            if (f == null) { println("NOFUNC " + a); continue; }
            DecompileResults res = ifc.decompileFunction(f, 180, monitor);
            if (!res.decompileCompleted()) { println("FAIL " + a + " " + res.getErrorMessage()); continue; }
            String c = res.getDecompiledFunction().getC();
            String fn = String.format("%08X.c", f.getEntryPoint().getOffset() & 0xFFFFFFFFL);
            try (PrintWriter w = new PrintWriter(new File(dir, fn), "UTF-8")) {
                w.println("// " + f.getName() + " @ 0x" + Long.toHexString(f.getEntryPoint().getOffset()));
                w.print(c);
            }
            String[] lines = c.split("\n");
            String sig = "";
            for (String l : lines) {
                if (l.contains("(") && !l.trim().startsWith("/*") && !l.trim().startsWith("*")
                        && !l.contains("=") && !l.contains(";")) { sig = l.trim(); break; }
            }
            println(String.format("%s  %s  size=%d  file=%s", a, sig, f.getBody().getNumAddresses(), fn));
        }
        ifc.dispose();
    }
}
