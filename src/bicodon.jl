__precompile__()
module Bicodon

using Measurements, Unitful, Bio
import Measurements: value, uncertainty
import Unitful: AbstractQuantity
import BioSequences
import GenomicFeatures
import BioAlignments
import BioStructures
import GeneticVariation
import BioServices
import BioTools

# TODO
#import Phylogenies

const Seq = BioSequences
const Intervals = GenomicFeatures
const Align = BioAlignments
const Structure = BioStructures
const Var = GeneticVariation
const Services = BioServices
const Tools = BioTools

# TODO
#const Phylo = Phylogenies

end  # module Bicodon
