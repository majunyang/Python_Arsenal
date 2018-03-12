select
d.dbid,
i.inst_id,i.instance_number,
d.name,d.db_unique_name,i.instance_name,
i.host_name,
d.current_scn,to_char(d.created,'yyyy-mm-dd hh24:mm:ss') "created",to_char(i.startup_time,'yyyy-mm-dd hh24:mm:ss') "Startup",
i.status,d.open_mode,i.database_status,
d.log_mode,d.force_logging,
d.flashback_on,
d.database_role,i.instance_role,
i.active_state,i.blocked,
d.protection_level,
i.version
from
gv$instance i,v$database d
where
i.instance_name=lower(d.name)