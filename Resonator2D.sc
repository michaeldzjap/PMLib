Resonator2D : ResonatorBase {
	var <epsilon;
	classvar <validBoundaryConds;

	*initClass {
		Class.initClassTree(Array); Class.initClassTree(Symbol);
		validBoundaryConds = #[
			'CCCC', 'CCCS', 'CCCF', 'CCSC', 'CCSS', 'CCSF', 'CCFC', 'CCFS', 'CCFF',
			'CSCC', 'CSCS', 'CSCF', 'CSSC', 'CSSS', 'CSSF', 'CSFC', 'CSFS', 'CSFF',
			'CFCC', 'CFCS', 'CFCF', 'CFSC', 'CFSS', 'CFSF', 'CFFC', 'CFFS', 'CFFF',
			'SCCC', 'SCCS', 'SCCF', 'SCSC', 'SCSS', 'SCSF', 'SCFC', 'SCFS', 'SCFF',
			'SSCC', 'SSCS', 'SSCF', 'SSSC', 'SSSS', 'SSSF', 'SSFC', 'SSFS', 'SSFF',
			'SFCC', 'SFCS', 'SFCF', 'SFSC', 'SFSS', 'SFSF', 'SFFC', 'SFFS', 'SFFF',
			'FCCC', 'FCCS', 'FCCF', 'FCSC', 'FCSS', 'FCSF', 'FCFC', 'FCFS', 'FCFF',
			'FSCC', 'FSCS', 'FSCF', 'FSSC', 'FSSS', 'FSSF', 'FSFC', 'FSFS', 'FSFF',
			'FFCC', 'FFCS', 'FFCF', 'FFSC', 'FFSS', 'FFSF', 'FFFC', 'FFFS', 'FFFF'];
	}

	*new { arg gamma=200,kappa=1,b1=0,b2=0,boundaryCond='SSSS',epsilon=1;
		^super.newCopyArgs(gamma,kappa,b1,b2,boundaryCond,epsilon).init(epsilon)
	}

	init { arg epsilon;
		this.epsilon = epsilon
	}

	epsilon_ { arg newEpsilon;
		(epsilon > 0).if {
			epsilon = newEpsilon
		} {
			Error("arg epsilon=% must be a real number greater than 0".format(newEpsilon)).throw
		}
	}

	boundaryCond_ { arg newBoundaryCond;
		validBoundaryConds.includes(newBoundaryCond).if {
			boundaryCond = newBoundaryCond
		} {
			Error("arg boundaryCond=% is not a valid 2D boundary condition".format(newBoundaryCond)).throw
		}
	}

	jsonString {
		var bcStr = boundaryCond.asString;
		bcStr = bcStr.toUpper;
		^"{ \"dim\":" ++ 2 ++ ",\"gamma\":" ++ gamma ++ ",\"kappa\":" ++ kappa ++ ",\"b1\":" ++ b1 ++ ",\"b2\":" ++ b2 ++ ",\"bc\":" ++ "\"" ++ bcStr ++ "\",\"epsilon\":" ++ epsilon ++ " }"
	}
}
