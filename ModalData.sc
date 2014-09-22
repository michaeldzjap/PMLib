ModalData {
	var <>modeFreqs,<>t60Times,<>biquadCoefs,<>numModes,<>numModesDiscarded,<>modeCalcTime;

	*new { arg modeFreqs,t60Times,biquadCoefs,numModes,numModesDiscarded,modeCalcTime;
		^super.newCopyArgs(modeFreqs,t60Times,biquadCoefs,numModes,numModesDiscarded,modeCalcTime)
	}

	// Discard all modes which have amplitude smaller than eps for efficiency
	discardModes { arg eps=1e-06,minFreq=25,maxFreq=(Server.default.sampleRate ? 44100).div(2);
		var i,result,dim,
		reduceModes = { |a1,a2|
			var tmpModeFreqs = Array.newClear(a1.size),tmpT60Times = Array.newClear(a1.size),
			tmpB1 = Array.newClear(a1.size), tmpB2 = Array.newClear(a1.size),
			tmpNumModes = Array.newClear(a1.size),tmpNumModesDiscarded = Array.newClear(a1.size);
			//try {
			a1 do: { |arr,j| var ind;
				tmpNumModesDiscarded[j] = arr.size;
				// extract all indices of the elms which are greater than eps in absolute value (this implies that a1 > eps and/or a2 > eps)
				ind = arr.indicesOfGreaterThanAbs(eps).union(a2[j].indicesOfGreaterThanAbs(eps)).sort;
				tmpModeFreqs[j] = modeFreqs|@|ind; tmpT60Times[j] = t60Times|@|ind;
				tmpB1[j] = biquadCoefs.b1|@|ind; tmpB2[j] = biquadCoefs.b2|@|ind;
				a1[j] = arr|@|ind; a2[j] = a2[j]|@|ind;
				// extract all indices of the elms which are greater than minFreq and less than maxFreq
				ind = tmpModeFreqs[j].indicesOfGreaterThan(minFreq).sect(tmpModeFreqs[j].indicesOfLessThan(maxFreq));
				tmpModeFreqs[j] = tmpModeFreqs[j]|@|ind; tmpT60Times[j] = tmpT60Times[j]|@|ind;
				tmpB1[j] = tmpB1[j]|@|ind; tmpB2[j] = (tmpB2[j]|@|ind).isNil.if { nil } { tmpB2[j]|@|ind };
				a1[j] = a1[j]|@|ind; a2[j] = a2[j]|@|ind;
				tmpNumModes[j] = ind.size;
				tmpNumModesDiscarded[j] = tmpNumModesDiscarded[j]-tmpNumModes[j]
			};
			/*} { |error|
				switch (error.species.name)
				{ 'DoesNotUnderstandError' } { Error("no modes found: try increasing the gain argument").throw }
				{ error.throw }
			};*/
			[tmpModeFreqs,tmpT60Times,a1,a2,tmpB1,tmpB2,tmpNumModes,tmpNumModesDiscarded]
		};

		biquadCoefs.a1[0].respondsTo('at').if {
			biquadCoefs.a1[0][0].respondsTo('at').if {
				dim = biquadCoefs.a1.size;
				result = dim collect: { |i| reduceModes.(biquadCoefs.a1[i],biquadCoefs.a2[i]) };
				modeFreqs = dim collect: { |i| result[i][0] }; t60Times = dim collect: { |i| result[i][1] };
				biquadCoefs.a1 = dim collect: { |i| result[i][2] }; biquadCoefs.a2 = dim collect: { |i| result[i][3] };
				biquadCoefs.b1 = dim collect: { |i| result[i][4] }; biquadCoefs.b2 = dim collect: { |i| result[i][5] };
				numModes = dim collect: { |i| result[i][6] }; numModesDiscarded = dim collect: { |i| result[i][7] }
			} {
				result = reduceModes.(biquadCoefs.a1,biquadCoefs.a2);
				modeFreqs = result[0]; t60Times = result[1];
				biquadCoefs.a1 = result[2]; biquadCoefs.a2 = result[3]; biquadCoefs.b1 = result[4]; biquadCoefs.b2 = result[5];
				numModes = result[6]; numModesDiscarded = result[7]
			}
		} {
			numModesDiscarded = 0; i = 0;
			while({ i < biquadCoefs.a1.size }) {
				(biquadCoefs.a1[i].abs < eps and: { biquadCoefs.a2[i].abs < eps } or: { modeFreqs[i] <= minFreq }
					or: { modeFreqs[i] >= maxFreq }).if {
					[modeFreqs,t60Times,biquadCoefs.a1,biquadCoefs.a2,biquadCoefs.b1,biquadCoefs.b2] do: _.removeAt(i);
					numModesDiscarded = numModesDiscarded+1
				} {
					i = i+1
				}
			};
			biquadCoefs.b2 = biquadCoefs.b2.clip2(0.999999);
			numModes = modeFreqs.size
		}
	}

}