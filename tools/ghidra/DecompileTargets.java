// Ghidra 12.x script: decompile a list of RVAs (image-base relative) and print C.
// Usage: -postScript DecompileTargets.java 0x350F20 0x34F970 ...
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class DecompileTargets extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        long base = currentProgram.getImageBase().getOffset();
        DecompInterface ifc = new DecompInterface();
        ifc.toggleCCode(true);
        ifc.toggleSyntaxTree(true);
        ifc.setSimplificationStyle("decompile");
        ifc.openProgram(currentProgram);

        for (String a : args) {
            long off = Long.parseLong(a.replace("0x", "").replace("0X", ""), 16);
            long va = (off >= base) ? off : base + off;
            Address addr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(va);
            Function f = getFunctionAt(addr);
            if (f == null) {
                f = getFunctionContaining(addr);
            }
            if (f == null) {
                println("===== NO FUNCTION at " + a + " (va 0x" + Long.toHexString(va) + ") =====");
                continue;
            }
            println("===== FUNCTION " + f.getName() + " @ 0x" + Long.toHexString(f.getEntryPoint().getOffset())
                    + " size " + f.getBody().getNumAddresses() + " =====");
            DecompileResults res = ifc.decompileFunction(f, 180, monitor);
            if (!res.decompileCompleted()) {
                println("DECOMP FAIL: " + res.getErrorMessage());
                continue;
            }
            println(res.getDecompiledFunction().getC());
            println("===== END " + f.getName() + " =====");
        }
        ifc.dispose();
    }
}
