ModalMorphData {
	var <>modeFreqs,<>dampingConsts,<>a1,<>a2,<>b1,<>b2,<>semitoneInterval,<identicalModesData,<transformedModesData,<uniqueModesData;

	*new { arg modeFreqs,dampingConsts,a1,a2,b1,b2,semitoneInterval;
		^super.newCopyArgs(modeFreqs,dampingConsts,a1,a2,b1,b2).init(semitoneInterval)
	}

	init { arg semitoneInterval;
		this.semitoneInterval = semitoneInterval ? 2;
		identicalModesData = List.new;
		transformedModesData = List.new;
		uniqueModesData = List.new
	}

	morphModes { arg morphMode=0;
		switch(morphMode,
			{ 0 }, { this.prMorphMethodOne }
		)
	}

	// private methods
	prMorphMethodOne {
		var identicalModes,uniqueModes,distMatrix;

		identicalModes = modeFreqs[0].sect(modeFreqs[1]);
		uniqueModes = [modeFreqs[0].difference(modeFreqs[1]),modeFreqs[1].difference(modeFreqs[0])];

		// collect filter coefficients of modes shared between the 2 objects
		(identicalModes.size > 0).if {
			2 do: { |i|
				identicalModes do: { |mode,j|
					// find all the indexes of the modes which are shared between the 2 objects
					var ind = modeFreqs[i].indexOf(mode);
					(i == 0).if {
						identicalModesData.add((modeFreq:mode,dampingConst:dampingConsts[0][ind],a1:[a1[0][ind],nil],a2:[a2[0][ind],nil],b1:b1[0][ind],b2:b2[0][ind]))
					} {
						// only numerator coefficients will be different, since mode frequencies remain the same
						identicalModesData[j].a1[1] = a1[1][ind];
						identicalModesData[j].a2[1] = a2[1][ind]
					}
				}
			}
		};

		// if both objects have unique modes, see which of them can be morphed into each other based on specified semitone interval limit (glissando)
		(uniqueModes[0].size > 0 and: { uniqueModes[1].size > 0 }).if {

			distMatrix = IdentityDictionary.new;

			// calculate the distance between every possible combination of unique modes belonging to one of the 2 objects
			uniqueModes[0] do: { |umode,j| var diff,diffMinItem,diffMinIndex;
				// calculate absolute difference in semitones between unique mode n of object 1 and all unique modes of object 2
				diff = (umode.cpsmidi - uniqueModes[1].cpsmidi).abs;
				// extract the smallest difference between unique mode n of object 1 and all unique modes of object 2
				diffMinItem = diff.minItem;
				// if this difference is smaller than our specified semitone limit, store both mode indices and the difference
				(diffMinItem < semitoneInterval).if {
					diffMinIndex = diff.minIndex;
					distMatrix.includesKey(diffMinIndex).if {
						distMatrix[diffMinIndex].add((objInd:j,diff:diffMinItem))
					} {
						distMatrix.add(diffMinIndex -> List.new.add((objInd:j,diff:diffMinItem)))
					}
				}
			};

			// find pairs of modes with the smallest distance between them and collect the result
			distMatrix keysValuesDo: { |key,val|
				var minIndex = val[val.performUnaryOp(\diff).minIndex].objInd,
				umodeFreq = [uniqueModes[0][minIndex],uniqueModes[1][key]],
				ind = 2 collect: { |i| modeFreqs[i].indexOf(umodeFreq[i]) };
				transformedModesData.add((modeFreq:umodeFreq,dampingConst:(2 collect: { |i| dampingConsts[i][ind[i]] }),a1:(2 collect: { |i| a1[i][ind[i]] }),a2:(2 collect: { |i| a2[i][ind[i]] }),b1:(2 collect: { |i| b1[i][ind[i]] }),b2:(2 collect: { |i| b2[i][ind[i]] })))
			};

			// remove all transformed modes, so all that is left are modes that should vanish
			2 do: { |i|
				(transformedModesData.size > 0).if {
					uniqueModes[i].removeAll(transformedModesData.performUnaryOp(\modeFreqs).flop[i])
				};
				uniqueModes[i] do: { |mode|
					var ind = modeFreqs[i].indexOf(mode);
					uniqueModesData.add((modeFreq:mode,dampingConst:dampingConsts[i][ind]));
					(i == 0).if {
						uniqueModesData.last.a1 = [a1[0][ind],0];
						uniqueModesData.last.a2 = [a2[0][ind],0];
						uniqueModesData.last.b1 = [b1[0][ind],0];
						uniqueModesData.last.b2 = [b2[0][ind],0]
					} {
						uniqueModesData.last.a1 = [0,a1[1][ind]];
						uniqueModesData.last.a2 = [0,a2[1][ind]];
						uniqueModesData.last.b1 = [0,b1[1][ind]];
						uniqueModesData.last.b2 = [0,b2[1][ind]]
					}
				}
			}
		} {
			// if only object 1 has unique modes, fade them out
			(uniqueModes[0].size > 0).if {
				uniqueModes[0] do: { |mode|
					var ind = modeFreqs[0].indexOf(mode);
					uniqueModesData.add((modeFreq:mode,dampingConst:dampingConsts[0][ind],a1:[a1[0][ind],0],a2:[a2[0][ind],0],b1:b1[0][ind],b2:b2[0][ind]))
				}
			} {
				// if only object 2 has unique modes, fade them in
				uniqueModes[1] do: { |mode|
					var ind = modeFreqs[1].indexOf(mode);
					uniqueModesData.add((modeFreq:mode,dampingConst:dampingConsts[1][ind],a1:[0,a1[1][ind]],a2:[0,a2[1][ind]],b1:b1[1][ind],b2:b2[1][ind]))
				}
			}
		}
	}

}