FDStringDesc : FDObjectBase {
	classvar <validBoundaryConds;

	*initClass {
		Class.initClassTree(Array);
		validBoundaryConds = #[\bothClamped,\leftClampedRightSimplySupported,\leftSimplySupportedRightClamped,\bothSimplySupported,\leftClampedRightFree,\leftFreeRightClamped,\leftSimplySupportedRightFree,\leftFreeRightSimplySupported,\bothFree]
	}

	boundaryCond_ { arg newBoundaryCond;
		validBoundaryConds.includes(newBoundaryCond).if {
			boundaryCond = newBoundaryCond
		} {
			Error("arg boundaryCond=% is not a valid 1D boundary condition".format(newBoundaryCond)).throw
		}
	}

	pythonString {
		var bcStr = boundaryCond.asString;
		bcStr[0] = bcStr[0].toUpper;
		^"FDString(" ++ gamma ++ "," ++ kappa ++ "," ++ b1 ++ "," ++ b2 ++ ",\"" ++ bcStr ++ "\")"
	}

}