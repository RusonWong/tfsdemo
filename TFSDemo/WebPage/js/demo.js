
$(function(){
	initDiskGraph(100);
	periodly_render();
});

//init block graph
function initDiskGraph(blockcount)
{
	for(i=0;i<blockcount;i++)
	{
		item = "<span class='block block_free' state='block_free' id='block_"+ i +"'>"+""+"</span>";
		$("#disk_main").append(item);
	}
}


/*
"Free":1
"Allocated":2
"Transparent":3
"Free_and_Overwritten":4
"Allocated_and_Overwritten":5
*/
function renderColor(states)
{
	statearr=[];
	statearr[1] ='block_free';
	statearr[2]='block_allocated';
	statearr[3]='block_transparent';
	statearr[4]='block_free_and_overwritten';
	statearr[5]='block_allocated_and_overwritten';
	
	for(i=0;i<states.length;i++)
	{
		stateidx = states[i];
		curClass = $("#block_"+i).attr("state");
		$("#block_"+i).removeClass(curClass);
		$("#block_"+i).addClass(statearr[stateidx]);
		$("#block_"+i).attr("state",statearr[stateidx]);
	}
}

function get_and_setDisk()
{
	$.ajax({
		url: '/monitor/states',
		type: 'GET',
		dataType: 'JSON',
		success: function(data){
			block_count = data.blockcount;
			states = data.states;
			renderColor(states);
		}
	});	
}

function periodly_render()
{
	get_and_setDisk();
	setTimeout(periodly_render,1000);
}

