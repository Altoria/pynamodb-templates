from datetime import datetime, timezone
from typing import Optional, Any, List, Dict, TypeVar, Type, Iterable, Sequence

from pynamodb.models import Model, Condition, OperationSettings, Action, ResultIterator

from pynamodb_templates.attributes import UnicodeDatetimeAttribute

_T = TypeVar("_T", bound="Model")
_KeyType = Any

__all__ = [
    "TimeTrackedModel",
    "CreatedAtTimeMixin",
    "ModifiedAtTimeMixin",
    "DeletedAtTimeMixin",
]


def utcnow():
    return datetime.now(tz=timezone.utc)


class CreatedAtTimeMixin(Model):
    created_at = UnicodeDatetimeAttribute(default_for_new=utcnow, force_utc=True)


class ModifiedAtTimeMixin(Model):
    modified_at = UnicodeDatetimeAttribute(default_for_new=utcnow, force_utc=True)

    def update(
        self,
        actions: List[Action],
        condition: Optional[Condition] = None,
        settings: OperationSettings = OperationSettings.default,
        update_timestamp: bool = True,
    ) -> Any:
        if update_timestamp:
            actions.append(self.__class__.modified_at.set(utcnow()))
        return super().update(actions=actions, condition=condition, settings=settings)

    def save(
        self,
        condition: Optional[Condition] = None,
        settings: OperationSettings = OperationSettings.default,
        update_timestamp: bool = True,
    ) -> Dict[str, Any]:
        if update_timestamp:
            self.modified_at = utcnow()
        return super().save(condition=condition, settings=settings)


class DeletedAtTimeMixin(Model):
    deleted_at = UnicodeDatetimeAttribute(null=True, force_utc=True)

    @classmethod
    def query(
        cls: Type[_T],
        hash_key: _KeyType,
        range_key_condition: Optional[Condition] = None,
        filter_condition: Optional[Condition] = None,
        ignore_deleted: bool = True,
        consistent_read: bool = False,
        index_name: Optional[str] = None,
        scan_index_forward: Optional[bool] = None,
        limit: Optional[int] = None,
        last_evaluated_key: Optional[Dict[str, Dict[str, Any]]] = None,
        attributes_to_get: Optional[Iterable[str]] = None,
        page_size: Optional[int] = None,
        rate_limit: Optional[float] = None,
        settings: OperationSettings = OperationSettings.default,
    ) -> ResultIterator[_T]:
        if ignore_deleted:
            if filter_condition is None:
                filter_condition = cls.deleted_at.does_not_exist()
            else:
                filter_condition = filter_condition & cls.deleted_at.does_not_exist()
        return super().query(
            hash_key=hash_key,
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            consistent_read=consistent_read,
            index_name=index_name,
            scan_index_forward=scan_index_forward,
            limit=limit,
            last_evaluated_key=last_evaluated_key,
            attributes_to_get=attributes_to_get,
            page_size=page_size,
            rate_limit=rate_limit,
            settings=settings,
        )

    @classmethod
    def scan(
        cls: Type[_T],
        filter_condition: Optional[Condition] = None,
        ignore_deleted: bool = True,
        segment: Optional[int] = None,
        total_segments: Optional[int] = None,
        limit: Optional[int] = None,
        last_evaluated_key: Optional[Dict[str, Dict[str, Any]]] = None,
        page_size: Optional[int] = None,
        consistent_read: Optional[bool] = None,
        index_name: Optional[str] = None,
        rate_limit: Optional[float] = None,
        attributes_to_get: Optional[Sequence[str]] = None,
        settings: OperationSettings = OperationSettings.default,
    ) -> ResultIterator[_T]:
        if ignore_deleted:
            if filter_condition is None:
                filter_condition = cls.deleted_at.does_not_exist()
            else:
                filter_condition = filter_condition & cls.deleted_at.does_not_exist()
        return super().scan(
            filter_condition=filter_condition,
            segment=segment,
            total_segments=total_segments,
            limit=limit,
            last_evaluated_key=last_evaluated_key,
            page_size=page_size,
            consistent_read=consistent_read,
            index_name=index_name,
            rate_limit=rate_limit,
            attributes_to_get=attributes_to_get,
            settings=settings,
        )

    def delete(
        self,
        force: bool = False,
        condition: Optional[Condition] = None,
        settings: OperationSettings = OperationSettings.default,
    ) -> Any:
        if force:
            return super().delete(condition=condition, settings=settings)
        else:
            actions = [self.__class__.deleted_at.set(utcnow())]
            return super().update(
                actions=actions, condition=condition, settings=settings
            )

    @property
    def is_deleted(self):
        return self.deleted_at is not None


class TimeTrackedModel(CreatedAtTimeMixin, ModifiedAtTimeMixin, DeletedAtTimeMixin):
    tz = timezone.utc


if __name__ == "__main__":
    from datetime import timezone, timedelta

    KST = timezone(timedelta(hours=9))

    class TimeTrackedModel(TimeTrackedModel):
        tz = KST

    m = TimeTrackedModel()

    print(m.serialize())
