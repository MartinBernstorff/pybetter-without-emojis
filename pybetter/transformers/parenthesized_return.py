import libcst as cst
import libcst.matchers as m
from libcst.metadata import PositionProvider

from pybetter.transformers.base import NoqaAwareTransformer


class RemoveParenthesesFromReturn(NoqaAwareTransformer):
    @m.call_if_inside(m.Return())
    @m.leave(m.Tuple(lpar=m.MatchIfTrue(lambda v: v is not None)))
    def remove_parentheses_from_return(
        self, original_node: cst.Tuple, updated_node: cst.Tuple
    ) -> cst.Tuple:

        # We get position of the `original_node`, since `updated_node` is
        # by definition different and was not processed by metadata provider.
        position: cst.metadata.CodeRange = self.get_metadata(
            PositionProvider, original_node
        )

        # Removing parentheses which are used to enable multi-line expression
        # will lead to invalid code, so we do nothing.
        if position.start.line != position.end.line:
            return original_node

        return updated_node.with_changes(lpar=[], rpar=[])


__all__ = ["RemoveParenthesesFromReturn"]
