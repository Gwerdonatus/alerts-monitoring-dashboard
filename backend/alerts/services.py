from typing import Set

from .models import Employee


def get_direct_report_ids(manager: Employee) -> Set[str]:
    """
    Get IDs of employees who directly report to the given manager.
    
    Args:
        manager: The Employee instance to get direct reports for
        
    Returns:
        Set of employee IDs that directly report to the manager
    """
    return set(manager.direct_reports.values_list('id', flat=True))


def get_subtree_report_ids(manager: Employee) -> Set[str]:
    """
    Get IDs of all employees in the manager's subtree (all descendants).
    
    Uses breadth-first search with cycle detection to safely traverse
    the org chart even if there are circular references.
    
    Args:
        manager: The Employee instance to get subtree reports for
        
    Returns:
        Set of all employee IDs in the manager's subtree
    """
    visited: Set[str] = set()
    queue = list(manager.direct_reports.values_list('id', flat=True))
    result: Set[str] = set()

    while queue:
        current_id = queue.pop(0)

        if current_id in visited:
            continue

        visited.add(current_id)
        result.add(current_id)

        children = Employee.objects.filter(reports_to_id=current_id)
        for child in children:
            if child.id not in visited:
                queue.append(child.id)

    return result
