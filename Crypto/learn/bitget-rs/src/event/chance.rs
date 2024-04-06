use crate::model::chance::TriangularArbitrageChance;
#[derive(Debug, clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum ChanceEvent {
    AllTaker(TriangularArbitrageChance),
    MakerTakerTaker(TriangularArbitrageChance),
}
