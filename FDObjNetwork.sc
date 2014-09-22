FDObjNetwork {
	var <objDescs,<connPointMatrix,<massMatrix,<excPointMatrix,<readoutPointMatrix,<modalData;
	classvar pythonScriptPath,<>pythonPath;

	*initClass {
		Class.initClassTree(String);
		pythonScriptPath = this.class.filenameSymbol.asString.dirname ++ "/python";
		pythonPath = "/Library/Frameworks/Python.framework/Versions/Current/bin"
	}

	*new { arg objDescs,connPointMatrix,massMatrix,excPointMatrix,readoutPointMatrix;
		^super.newCopyArgs(objDescs,connPointMatrix,massMatrix,excPointMatrix,readoutPointMatrix)
		.init(objDescs,connPointMatrix,massMatrix,excPointMatrix,readoutPointMatrix)
	}

	init { arg objDescs,connPointMatrix,massMatrix,excPointMatrix,readoutPointMatrix;
		this.objDescs = objDescs ? [FDStringDesc.new,FDStringDesc.new(101)];
		this.connPointMatrix = connPointMatrix ? Array2D.fromArray(2,1,[0.5,0.5]);
		this.massMatrix = massMatrix ? Array2D.fromArray(2,1,[1,1]);
		this.excPointMatrix = excPointMatrix ? Array2D.fromArray(2,1,[0.25,0]);
		this.readoutPointMatrix = readoutPointMatrix ? Array2D.fromArray(2,1,[0.5,0])
	}

	objDescs_ { arg newObjDescs;
		(newObjDescs.size == 0).if { newObjDescs = [newObjDescs].asList };
		newObjDescs.respondsTo('values').if { newObjDescs = newObjDescs.values };
		newObjDescs.isKindOf(Array).if { newObjDescs = newObjDescs.asList };
		objDescs = newObjDescs
	}

	connPointMatrix_ { arg newConnPointMatrix;
		newConnPointMatrix.respondsTo('rows').if {
			connPointMatrix = newConnPointMatrix
		} {
			(newConnPointMatrix.shape.size != 2).if {
				Error("arg connPointMatrix=% must be a 2D indexable collection".format(newConnPointMatrix)).throw
			} {
				(newConnPointMatrix any: { |arr| arr.size != newConnPointMatrix[0].size }).if {
					Error("arg connPointMatrix=% must contain equal sized rows".format(newConnPointMatrix)).throw
				} {
					connPointMatrix = newConnPointMatrix
				}
			}
		}
	}

	massMatrix_ { arg newMassMatrix;
		newMassMatrix.respondsTo('rows').if {
			massMatrix = newMassMatrix
		} {
			(newMassMatrix.shape.size != 2).if {
				Error("arg massMatrix=% must be a 2D indexable collection".format(newMassMatrix)).throw
			} {
				(newMassMatrix any: { |arr| arr.size != newMassMatrix[0].size }).if {
					Error("arg massMatrix=% must contain equal sized rows".format(newMassMatrix)).throw
				} {
					massMatrix = newMassMatrix
				}
			}
		}
	}

	excPointMatrix_ { arg newExcPointMatrix;
		newExcPointMatrix.respondsTo('rows').if {
			excPointMatrix = newExcPointMatrix
		} {
			(newExcPointMatrix.shape.size != 2).if {
				Error("arg excPointMatrix=% must be a 2D indexable collection".format(newExcPointMatrix)).throw
			} {
				(newExcPointMatrix any: { |arr| arr.size != newExcPointMatrix[0].size }).if {
					Error("arg excPointMatrix=% must contain equal sized rows".format(newExcPointMatrix)).throw
				} {
					excPointMatrix = newExcPointMatrix
				}
			}
		}
	}

	readoutPointMatrix_ { arg newReadoutPointMatrix;
		newReadoutPointMatrix.respondsTo('rows').if {
			readoutPointMatrix = newReadoutPointMatrix
		} {
			(newReadoutPointMatrix.shape.size != 2).if {
				Error("arg readoutPointMatrix=% must be a 2D indexable collection".format(newReadoutPointMatrix)).throw
			} {
				(newReadoutPointMatrix any: { |arr| arr.size != newReadoutPointMatrix[0].size }).if {
					Error("arg readoutPointMatrix=% must contain equal sized rows".format(newReadoutPointMatrix)).throw
				} {
					readoutPointMatrix = newReadoutPointMatrix
				}
			}
		}
	}

	/*
	addMechObjDesc { arg item;
		this.objDescs.add(item)
	}

	insertMechObjDesc { arg index,item;
		this.objDescs.insert(index,item)
	}

	replaceMechObjDesc { arg index,item;
		this.objDescs[index] = item
	}

	removeMechObjDesc { arg index;
		^this.objDescs.removeAt(index)
	}
	*/

	calcModes { arg eps=1e-06,minFreq=25,maxFreq=(Server.default.sampleRate ? 44100).div(2),gain=1;
		this.prCheckMatrixDimensions;
		this.prParseSCArgs(gain);
		// have to use systemCmd instead of unixCmd here, since we want synchronous execution
		("export PATH=" ++ pythonPath ++ ":$PATH && cd" + pythonScriptPath + "&& python systemSetup.py").systemCmd;
		this.prParsePythonOutput;
		("cd" + pythonScriptPath + "&& rm -rf networkArgs.txt").systemCmd;
		modalData.discardModes(eps,minFreq,maxFreq)
	}

	saveObjNetwork { arg pathname=this.class.filenameSymbol.asString.dirname ++ "/networkSettings.scd";
		var settings = IdentityDictionary.new.add(\objSettings -> Array.newClear(this.objDescs.size));
		this.objDescs do: { |obj,i|
			settings[\objSettings][i] = IdentityDictionary.new.add(\className -> obj.class.asSymbol);
			obj.class.instVarNames do: { |instVarName| settings[\objSettings][i].add(instVarName -> obj.perform(instVarName)) }
		};
		settings.add(\networkSettings -> IdentityDictionary.new.add(\connPointMatrix -> this.connPointMatrix).add(\massMatrix -> this.massMatrix)
			.add(\excPointMatrix -> this.excPointMatrix).add(\readoutPointMatrix -> this.readoutPointMatrix).add(\numModes -> modalData.numModes)
			.add(\numModesDiscarded -> modalData.numModesDiscarded).add(\modeCalcTime -> modalData.modeCalcTime)
		);
		// store mode frequencies, t60 times and filter coefficients with highest possible precision
		settings[\networkSettings].add(\modeFreqs -> modalData.modeFreqs.deepCollect(modalData.modeFreqs.shape.size,{ |item| [item.high32Bits,item.low32Bits] }));
		settings[\networkSettings].add(\t60Times -> modalData.t60Times.deepCollect(modalData.t60Times.shape.size,{ |item| [item.high32Bits,item.low32Bits] }));
		modalData.biquadCoefs keysValuesDo: { |key,val|
			settings[\networkSettings].add(key -> val.deepCollect(val.shape.size,{ |item| [item.high32Bits,item.low32Bits] }))
		};
		// TO DO: SAVE MORPH BIQUAD COEFFICIENTS IF ANY ARE SPECIFIED!!!
		settings.writeArchive(pathname)
	}

	*loadObjNetwork { arg pathname=this.class.filenameSymbol.asString.dirname ++ "/networkSettings.scd";
		var settings = Object.readArchive(pathname),nw;
		nw = FDObjNetwork(*(
			[settings[\objSettings] collect: { |dict| dict[\className].asClass.new(*dict.atAll(dict[\className].asClass.instVarNames)) }]
			++ settings[\networkSettings].atAll([\connPointMatrix,\massMatrix,\excPointMatrix,\readoutPointMatrix])
		));
		^nw.prSetNetworkSettings(*settings[\networkSettings].atAll([\modeFreqs,\t60Times,\a1,\a2,\b1,\b2,\numModes,\numModesDiscarded,\modeCalcTime]))
	}

	/*
	 *******************
	 * PRIVATE METHODS *
	 *******************
	 */
	prCheckMatrixDimensions {
		var err=Error("matrix must have the same nr. of rows as there are items in objDescs");
		[connPointMatrix,massMatrix,excPointMatrix,readoutPointMatrix] do: { |mtr|
			var op = mtr.respondsTo('rows').if { 'rows' } { 'size' };
			(mtr.perform(op) != objDescs.size).if { err.throw }
		};
		err=Error("args connPointMatrix and massMatrix must have the same dimensions");
		(connPointMatrix.respondsTo('rows') and: { massMatrix.respondsTo('rows') }).if {
			(connPointMatrix.rows == massMatrix.rows and: { connPointMatrix.cols == massMatrix.cols }).not.if { err.throw }
		} {
			(connPointMatrix.respondsTo('rows') and: { massMatrix.respondsTo('rows').not }).if {
				(connPointMatrix.rows == massMatrix.size and: { connPointMatrix.cols == massMatrix[0].size }).not.if { err.throw }
			} {
				(connPointMatrix.respondsTo('rows').not and: { massMatrix.respondsTo('rows') }).if {
					(connPointMatrix.size == massMatrix.rows and: { connPointMatrix[0].size == massMatrix.cols }).not.if { err.throw }
				} {
					(connPointMatrix.shape != massMatrix.shape).if { err.throw }
				}
			}
		}
	}

	prParseSCArgs { arg gain; var file,str;
		File.use(pythonScriptPath ++ "/networkArgs.txt","w", { |f|
			str = "[";
			objDescs do: { |obj,i| str = str ++ obj.pythonString ++ (i == objDescs.lastIndex).if { "]\n" } { "," } };
			f.write(str);
			[connPointMatrix,massMatrix,excPointMatrix,readoutPointMatrix] do: { |mtr,i| i=i+1;
				str = "array([";
				mtr.isKindOf(Array2D).if {
					mtr rowsDo: { |row,j| str = str ++ row ++ (j == (mtr.rows-1)).if { "])\n" } { "," } }
				} {
					mtr do: { |row,j| str = str ++ row ++ (j == (mtr.size-1)).if { "])\n" } { "," } }
				};
				f.write(str)
			};
			f.write(gain.asString)
		})
	}

	prParsePythonOutput { var file,readFunc,modeFreqs,t60Times,biquadCoefs,modeCalcTime;
		file = File(pythonScriptPath ++ "/modalData.txt","r");
		readFunc = { var str="";
			while({ str.contains("&").not }) {
				str = str ++ file.getLine
			};
			str = str.replace("&","");
			str.interpret
		};
		modeFreqs = readFunc.value;
		t60Times = readFunc.value;
		biquadCoefs = (a1:readFunc.value,a2:readFunc.value,b1:readFunc.value,b2:readFunc.value);
		modeCalcTime = file.getLine.interpret;
		file.close;
		("cd" + pythonScriptPath + "&& rm -rf modalData.txt").systemCmd;
		modalData = ModalData(modeFreqs,t60Times,biquadCoefs).modeCalcTime_(modeCalcTime)
	}

	prSetNetworkSettings { arg newModeFreqs,newT60Times,newA1,newA2,newB1,newB2,newNumModes,newNumModesDiscarded,newModeCalcTime;
		modalData = ModalData(
			newModeFreqs.deepCollect(newModeFreqs.shape.size-1,{ |item| Float.from64Bits(*item) }),
			newT60Times.deepCollect(newT60Times.shape.size-1,{ |item| Float.from64Bits(*item) }),
			(
				a1:newA1.deepCollect(newA1.shape.size-1,{ |item| Float.from64Bits(*item) }),
				a2:newA2.deepCollect(newA2.shape.size-1,{ |item| Float.from64Bits(*item) }),
				b1:newB1.deepCollect(newB1.shape.size-1,{ |item| Float.from64Bits(*item) }),
				b2:newB2.deepCollect(newB2.shape.size-1,{ |item| Float.from64Bits(*item) })
			),
			newNumModes,
			newNumModesDiscarded,
			newModeCalcTime
		)
	}

}

+ SequenceableCollection {
	indicesOfNotEqual { |item|
		var indices=Array.new;
		this.do { arg val, i;
			if (item != val) { indices = indices.add(i) }
		};
		^indices
	}

	indicesOfLessThan { |item|
		var indices=Array.new;
		this.do { arg val, i;
			if (item >= val) { indices = indices.add(i) }
		};
		^indices
	}

	indicesOfLessThanAbs { |item|
		var indices=Array.new;
		this.do { arg val, i;
			if (item.abs >= val.abs) { indices = indices.add(i) }
		};
		^indices
	}

	indicesOfGreaterThan { |item|
		var indices=Array.new;
		this.do { arg val, i;
			if (item <= val) { indices = indices.add(i) }
		};
		^indices
	}

	indicesOfGreaterThanAbs { |item|
		var indices=Array.new;
		this.do { arg val, i;
			if (item.abs <= val.abs) { indices = indices.add(i) }
		};
		^indices
	}
}