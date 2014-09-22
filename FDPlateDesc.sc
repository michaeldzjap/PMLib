FDPlateDesc : FDObjectBase {
	var <epsilon,<nu;
	classvar <validBoundaryConds;

	*initClass {
		Class.initClassTree(Array); Class.initClassTree(Symbol);
		/*validBoundaryConds = List.new;
		[\Clamped,\SimplySupported,\Free] do: { |sym0|
			[\Clamped,\SimplySupported,\Free] do: { |sym1|
				[\Clamped,\SimplySupported,\Free] do: { |sym2|
					[\Clamped,\SimplySupported,\Free] do: { |sym3|
						(sym0 == sym1 and: { sym1 == sym2 } and: { sym2 == sym3 }).if {
							validBoundaryConds.add(\allSides++sym0)
						} {
							validBoundaryConds.add(\left++sym0++\Right++sym1++\Top++sym2++\Bottom)
						}
					}
				}
			}
		}*/
		validBoundaryConds = #[\allSidesClamped,\leftClampedRightClampedTopClampedBottom,\leftClampedRightClampedTopClampedBottom,\leftClampedRightClampedTopSimplySupportedBottom,\leftClampedRightClampedTopSimplySupportedBottom,\leftClampedRightClampedTopSimplySupportedBottom,\leftClampedRightClampedTopFreeBottom,\leftClampedRightClampedTopFreeBottom,\leftClampedRightClampedTopFreeBottom,\leftClampedRightSimplySupportedTopClampedBottom,\leftClampedRightSimplySupportedTopClampedBottom,\leftClampedRightSimplySupportedTopClampedBottom,\leftClampedRightSimplySupportedTopSimplySupportedBottom,\leftClampedRightSimplySupportedTopSimplySupportedBottom,\leftClampedRightSimplySupportedTopSimplySupportedBottom,\leftClampedRightSimplySupportedTopFreeBottom,\leftClampedRightSimplySupportedTopFreeBottom,\leftClampedRightSimplySupportedTopFreeBottom,\leftClampedRightFreeTopClampedBottom,\leftClampedRightFreeTopClampedBottom,\leftClampedRightFreeTopClampedBottom,\leftClampedRightFreeTopSimplySupportedBottom,\leftClampedRightFreeTopSimplySupportedBottom,\leftClampedRightFreeTopSimplySupportedBottom,\leftClampedRightFreeTopFreeBottom,\leftClampedRightFreeTopFreeBottom,\leftClampedRightFreeTopFreeBottom,\leftSimplySupportedRightClampedTopClampedBottom,\leftSimplySupportedRightClampedTopClampedBottom,\leftSimplySupportedRightClampedTopClampedBottom,\leftSimplySupportedRightClampedTopSimplySupportedBottom,\leftSimplySupportedRightClampedTopSimplySupportedBottom,\leftSimplySupportedRightClampedTopSimplySupportedBottom,\leftSimplySupportedRightClampedTopFreeBottom,\leftSimplySupportedRightClampedTopFreeBottom,\leftSimplySupportedRightClampedTopFreeBottom,\leftSimplySupportedRightSimplySupportedTopClampedBottom,\leftSimplySupportedRightSimplySupportedTopClampedBottom,\leftSimplySupportedRightSimplySupportedTopClampedBottom,\leftSimplySupportedRightSimplySupportedTopSimplySupportedBottom,\allSidesSimplySupported,\leftSimplySupportedRightSimplySupportedTopSimplySupportedBottom,\leftSimplySupportedRightSimplySupportedTopFreeBottom,\leftSimplySupportedRightSimplySupportedTopFreeBottom,\leftSimplySupportedRightSimplySupportedTopFreeBottom,\leftSimplySupportedRightFreeTopClampedBottom,\leftSimplySupportedRightFreeTopClampedBottom,\leftSimplySupportedRightFreeTopClampedBottom,\leftSimplySupportedRightFreeTopSimplySupportedBottom,\leftSimplySupportedRightFreeTopSimplySupportedBottom,\leftSimplySupportedRightFreeTopSimplySupportedBottom,\leftSimplySupportedRightFreeTopFreeBottom,\leftSimplySupportedRightFreeTopFreeBottom,\leftSimplySupportedRightFreeTopFreeBottom,\leftFreeRightClampedTopClampedBottom,\leftFreeRightClampedTopClampedBottom,\leftFreeRightClampedTopClampedBottom,\leftFreeRightClampedTopSimplySupportedBottom,\leftFreeRightClampedTopSimplySupportedBottom,\leftFreeRightClampedTopSimplySupportedBottom,\leftFreeRightClampedTopFreeBottom,\leftFreeRightClampedTopFreeBottom,\leftFreeRightClampedTopFreeBottom,\leftFreeRightSimplySupportedTopClampedBottom,\leftFreeRightSimplySupportedTopClampedBottom,\leftFreeRightSimplySupportedTopClampedBottom,\leftFreeRightSimplySupportedTopSimplySupportedBottom,\leftFreeRightSimplySupportedTopSimplySupportedBottom,\leftFreeRightSimplySupportedTopSimplySupportedBottom,\leftFreeRightSimplySupportedTopFreeBottom,\leftFreeRightSimplySupportedTopFreeBottom,\leftFreeRightSimplySupportedTopFreeBottom,\leftFreeRightFreeTopClampedBottom,\leftFreeRightFreeTopClampedBottom,\leftFreeRightFreeTopClampedBottom,\leftFreeRightFreeTopSimplySupportedBottom,\leftFreeRightFreeTopSimplySupportedBottom,\leftFreeRightFreeTopSimplySupportedBottom,\leftFreeRightFreeTopFreeBottom,\leftFreeRightFreeTopFreeBottom,\allSidesFree]
	}

	*new { arg gamma=200,kappa=1,b1=0,b2=0,boundaryCond=\allSidesSimplySupported,epsilon=1,nu=1;
		^super.newCopyArgs(gamma,kappa,b1,b2,boundaryCond,epsilon,nu).init(epsilon,nu)
	}

	init { arg epsilon,nu;
		this.epsilon = epsilon;
		this.nu = nu
	}

	epsilon_ { arg newEpsilon;
		(epsilon > 0).if {
			epsilon = newEpsilon
		} {
			Error("arg epsilon=% must be a real number greater than 0".format(newEpsilon)).throw
		}
	}

	nu_ { arg newNu;
		nu = newNu
	}

	boundaryCond_ { arg newBoundaryCond;
		validBoundaryConds.includes(newBoundaryCond).if {
			boundaryCond = newBoundaryCond
		} {
			Error("arg boundaryCond=% is not a valid 2D boundary condition".format(newBoundaryCond)).throw
		}
	}

	pythonString {
		var bcStr = boundaryCond.asString;
		bcStr[0] = bcStr[0].toUpper;
		^"FDPlate(" ++ gamma ++ "," ++ kappa ++ "," ++ b1 ++ "," ++ b2 ++ ",\"" ++ bcStr ++ "\"," ++ epsilon ++ "," ++ nu ++ ")"
	}
}